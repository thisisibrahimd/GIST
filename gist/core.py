import datetime
import logging
import numpy as np
import math
from sklearn import svm
from sklearn import preprocessing
from functools import reduce

logger = logging.getLogger(__name__)

AGE_CONCEPT_ID = 4265453
GENDER_CONCEPT_ID = 4135376
MALE_GENDER_CONCEPT_ID = 8507
FEMALE_GENDER_CONCEPT_ID = 8532

def get_gist_score(trial_id, criteria, ehr):
    lab_criteria = list(filter(lambda criterion: criterion.domain_id == "Measurement" or criterion.concept_id == AGE_CONCEPT_ID, criteria))

    lab_stats = get_lab_stats(lab_criteria, ehr)
    logger.info(f"calculated {len(lab_stats)} lab stats")

    features, labels = get_features_and_labels(lab_stats, ehr)
    weights = get_weights(features, labels)
    logger.info(f"calculated {len(weights)} weights")

    elig_checks = get_elig_checks(criteria, ehr)
    logger.info(f"checked eligibility for {len(elig_checks)} EHRs")

    gist_score = {
        'trial_id': trial_id
    }
    gist_score['s_gist_scores'] = get_s_gist_scores(criteria, elig_checks, weights)

    if (any(s_gist_score['score'] == 0 for s_gist_score in gist_score['s_gist_scores'])):
        zero_s_gist_scores = list(filter(lambda s_gist_score: s_gist_score['score'] == 0, gist_score['s_gist_scores']))
        logger.info(f"found {len(zero_s_gist_scores)} s_gist_score(s) with a score of zero")
        zero_concept_ids = list(map(lambda s_gist_score: s_gist_score['concept_id'], zero_s_gist_scores))
        logger.info(f"removing {zero_concept_ids} from analysis")
        new_criteria = list(filter(lambda criterion: criterion.concept_id not in zero_concept_ids, criteria))

        new_elig_checks = get_elig_checks(new_criteria, ehr)
        gist_score['m_gist_score'] = get_m_gist_score(new_elig_checks, weights)
    else:
        logger.info("no zeros in s gist scores found")
        gist_score['m_gist_score'] = get_m_gist_score(elig_checks, weights)
    return gist_score

def get_lab_stats(lab_criteria, ehr):
    lab_stats = {}
    for lab_criterion in lab_criteria:
        lab_stats[lab_criterion.concept_id] = {
            'criterion': lab_criterion
        }
        values = []

        if (lab_criterion.concept_id == AGE_CONCEPT_ID):
            values = list(map(lambda person: datetime.date.today().year - person.year_of_birth, ehr))
        else:
            measurements_by_criterion = list(map(lambda person: reduce(lambda m1, m2: m1 if m1.measurement_concept_id == lab_criterion.concept_id else m2, person.measurement), ehr))
            values = list(map(lambda measurement: measurement.value_as_number, measurements_by_criterion))

        lab_stats[lab_criterion.concept_id]['mean'] = float(sum(values) / len(values))
        lab_stats[lab_criterion.concept_id]['inelig_prec'] = float(len(list(filter(lambda value: lab_criterion.lab_elig_min >= value or value >= lab_criterion.lab_elig_max, values))) / len(values))
        square_diff = list(map(lambda value: pow(float(value) - lab_stats[lab_criterion.concept_id]['mean'], 2), values))
        lab_stats[lab_criterion.concept_id]['std_dev'] = float(math.sqrt(sum(square_diff) / len(square_diff)))
        lab_stats[lab_criterion.concept_id]['norm_min'] = float(lab_criterion.lab_elig_min - lab_stats[lab_criterion.concept_id]['mean'] / lab_stats[lab_criterion.concept_id]['std_dev'])
        lab_stats[lab_criterion.concept_id]['norm_max'] = float(lab_criterion.lab_elig_max - lab_stats[lab_criterion.concept_id]['mean'] / lab_stats[lab_criterion.concept_id]['std_dev'])
    return lab_stats


def get_features_and_labels(lab_stats, ehr):
    features = []
    labels = []
    for person in ehr:
        feature = []
        for lab_concept_id, lab_stat in lab_stats.items():
            if (lab_concept_id == AGE_CONCEPT_ID):
                age = datetime.date.today().year - person.year_of_birth
                weighed_age = age - lab_stat['mean'] / lab_stat['std_dev'] * lab_stat['inelig_prec']
                labels.append(weighed_age)
            else:
                exists = any(measurement.measurement_concept_id == lab_concept_id for measurement in person.measurement)
                if (exists):
                    value = float(reduce(lambda m1, m2: m1 if m1.measurement_concept_id == lab_concept_id else m2, person.measurement).value_as_number)
                    try:
                        weighted_value = (value - lab_stat['mean']) / (lab_stat['std_dev'] * lab_stat['inelig_prec'])
                        feature.append(weighted_value)
                    except ZeroDivisionError:
                        feature.append(0)
                else:
                    default_value = float((lab_stat['criterion']['lab_elig_max'] - lab_stat['criterion']['lab_elig_min']) / 2 * lab_stat['criterion']['lab_elig_min'])
                    weighted_value = default_value - lab_stat['mean'] / lab_stat['std_dev'] * lab_stat['inelig_prec']
                    feature.append(weighted_value)
        features.append(feature)
    return (features, labels)


def get_weights(features, labels):
    features = np.array(features)
    labels = np.array(labels)

    lab_enc = preprocessing.LabelEncoder()
    encoded_labels = lab_enc.fit_transform(labels)
    clf = svm.SVC(gamma='auto')
    clf.fit(features, encoded_labels)

    predictions = clf.predict(features)
    predictions_recovered = lab_enc.inverse_transform(predictions)
    result = list(predictions_recovered)

    weights = list(map(lambda tuple: 1 / (1 + abs(tuple[0] - tuple[1])), zip(result, labels)))
    return weights


def check_categorical_value(criterion, value):
    if (criterion.lab_elig_min <= value and value <= criterion.lab_elig_max and criterion.cat_elig == 1):
        return True
    elif ((criterion.lab_elig_min > value or value > criterion.lab_elig_max) and criterion.cat_elig == 0):
        return True
    return False


def get_elig_checks(criteria, ehr):
    elig_checks = []
    for person in ehr:
        elig_check = {
            'person_id': person.person_id,
            'checks': {}
        }
        for criterion in criteria:
            elig_check['checks'][criterion.concept_id] = {
                'criterion': criterion,
            }

            if (criterion.concept_id == GENDER_CONCEPT_ID):
                gender_concept_id = person.gender_source_concept_id
                if (criterion.cat_elig == 0):
                    elig_check['checks'][criterion.concept_id]['is_eligible'] = True
                elif (criterion.cat_elig == 1 and gender_concept_id == MALE_GENDER_CONCEPT_ID):
                    elig_check['checks'][criterion.concept_id]['is_eligible'] = True
                elif (criterion.cat_elig == 2 and gender_concept_id == FEMALE_GENDER_CONCEPT_ID):
                    elig_check['checks'][criterion.concept_id]['is_eligible'] = True
                else:
                    elig_check['checks'][criterion.concept_id]['is_eligible'] = False
            elif (criterion.concept_id == AGE_CONCEPT_ID):
                age = datetime.date.today().year - person.year_of_birth
                elig_check['checks'][criterion.concept_id]['is_eligible'] = check_categorical_value(criterion, age)
            elif (criterion.domain_id == "Condition" or criterion.domain_id == "Drug" or criterion.domain_id == "Procedure" or (criterion.domain_id == "Observation" and criterion.concept_id != 4265453)):
                if (criterion.domain_id == "Condition"):
                    elig_check['checks'][criterion.concept_id]['is_eligible'] = any(condition.condition_concept_id == criterion.concept_id for condition in person.condition_occurrence)
                elif (criterion.domain_id == "Drug"):
                    elig_check['checks'][criterion.concept_id]['is_eligible'] = any(drug.drug_concept_id == criterion.concept_id for drug in person.drug_exposure)
                elif (criterion.domain_id == "Obseration"):
                    elig_check['checks'][criterion.concept_id]['is_eligible'] = any(observation.observation_concept_id == criterion.concept_id for observation in person.observation)
                elif (criterion.domain_id == "Procedure"):
                    elig_check['checks'][criterion.concept_id]['is_eligible'] = any(procedure.procedure_concept_id == criterion.concept_id for procedure in person.procedure_occurrence)
                else:
                    elig_check['checks'][criterion.concept_id]['is_eligible'] = False
            else:
                value = reduce(lambda m1, m2: m1 if m1.measurement_concept_id == criterion.concept_id else m2, person.measurement).value_as_number
                elig_check['checks'][criterion.concept_id]['is_eligible'] = check_categorical_value(criterion, value)
        elig_checks.append(elig_check)
    return elig_checks


def get_s_gist_scores(criteria, elig_checks, weights):
    s_gist_scores = []
    sum_weights = sum(weights)
    for criterion in criteria:
        s_gist_score = get_s_gist_score(criterion, elig_checks, weights, sum_weights)
        s_gist_scores.append(s_gist_score)
    return s_gist_scores



def get_s_gist_score(criterion, elig_checks, weights, sum_weights):
    s_gist_score = {
        'concept_id': criterion.concept_id
    }
    checks = list(map(lambda elig_check: int(elig_check['checks'][criterion.concept_id]['is_eligible']), elig_checks))
    weight_checks = list(map(lambda tuple: tuple[0] * tuple[1], zip(checks, weights)))
    s_gist_score['score'] = sum(weight_checks) / sum_weights
    return s_gist_score


def get_m_gist_score(elig_checks, weights):
    num_fully_eligible = len(list(filter(lambda elig_check: all(map(lambda check: check['is_eligible'], elig_check['checks'].values())), elig_checks)))
    logger.debug(f'Number of Fully Eligible People: {num_fully_eligible}')
    score = num_fully_eligible / sum(weights)
    return score