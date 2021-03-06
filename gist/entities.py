# coding: utf-8
from sqlalchemy import CheckConstraint, Column, Integer, BigInteger, Date, DateTime, ForeignKey, Numeric, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base




################################################################
#              START of DB tables for Criteria DB              #
################################################################


CritBase = declarative_base()
crit_metadata = CritBase.metadata

class EligibilityCriterion(CritBase):
    __tablename__ = 'eligibility_criterion'
    __table_args__ = (
        CheckConstraint("((domain_id)::text = 'Measurement'::text) OR ((domain_id)::text = 'Observation'::text) OR ((domain_id)::text = 'Procedure'::text) OR ((domain_id)::text = 'Condition'::text) OR ((domain_id)::text = 'Drug'::text)"),
        CheckConstraint('((lab_elig_min IS NULL) AND (lab_elig_max IS NULL)) OR (NOT ((lab_elig_min IS NULL) AND (lab_elig_max IS NULL)))')
    )

    nct_id = Column(String(255), primary_key=True, nullable=False)
    concept_name = Column(String(255))
    concept_id = Column(Integer, primary_key=True, nullable=False)
    domain_id = Column(String(255), nullable=False)
    cat_elig = Column(Integer, nullable=False)
    lab_elig_min = Column(Integer)
    lab_elig_max = Column(Integer)

    def __repr__(self):
        return f"EligibilityCriterion(nct_id='{self.nct_id}', concept_id='{self.concept_id}', domain_id='{self.domain_id}')"


################################################################
#               END of DB tables for Criteria DB               #
################################################################





################################################################
#                 START of DB tables for EHR DB                #
################################################################


EhrBase = declarative_base()
ehr_metadata = CritBase.metadata


class Person(EhrBase):
    __tablename__ = 'person'

    person_id = Column(Integer, primary_key=True, unique=True)
    gender_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    year_of_birth = Column(Integer, nullable=False)
    month_of_birth = Column(Integer)
    day_of_birth = Column(Integer)
    birth_datetime = Column(DateTime)
    race_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    ethnicity_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    location_id = Column(ForeignKey('location.location_id'))
    provider_id = Column(ForeignKey('provider.provider_id'))
    care_site_id = Column(ForeignKey('care_site.care_site_id'))
    person_source_value = Column(String(50))
    gender_source_value = Column(String(50))
    gender_source_concept_id = Column(ForeignKey('concept.concept_id'))
    race_source_value = Column(String(50))
    race_source_concept_id = Column(ForeignKey('concept.concept_id'))
    ethnicity_source_value = Column(String(50))
    ethnicity_source_concept_id = Column(ForeignKey('concept.concept_id'))

    care_site = relationship('CareSite')
    ethnicity_concept = relationship('Concept', primaryjoin='Person.ethnicity_concept_id == Concept.concept_id')
    ethnicity_source_concept = relationship('Concept', primaryjoin='Person.ethnicity_source_concept_id == Concept.concept_id')
    gender_concept = relationship('Concept', primaryjoin='Person.gender_concept_id == Concept.concept_id')
    gender_source_concept = relationship('Concept', primaryjoin='Person.gender_source_concept_id == Concept.concept_id')
    location = relationship('Location')
    provider = relationship('Provider')
    race_concept = relationship('Concept', primaryjoin='Person.race_concept_id == Concept.concept_id')
    race_source_concept = relationship('Concept', primaryjoin='Person.race_source_concept_id == Concept.concept_id')

    condition_occurrence = relationship('ConditionOccurrence')
    drug_exposure = relationship('DrugExposure')
    procedure_occurrence = relationship('ProcedureOccurrence')
    measurement = relationship('Measurement')
    observation = relationship('Observation')

    def __repr__(self):
        return f"Person(person_id='{self.person_id}', gender_id='{self.gender_concept_id}', year_of_birth='{self.year_of_birth}')"


class ConditionOccurrence(EhrBase):
    __tablename__ = 'condition_occurrence'

    condition_occurrence_id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    condition_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    condition_start_date = Column(Date, nullable=False)
    condition_start_datetime = Column(DateTime, nullable=False)
    condition_end_date = Column(Date)
    condition_end_datetime = Column(DateTime)
    condition_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    stop_reason = Column(String(20))
    provider_id = Column(ForeignKey('provider.provider_id'))
    visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'), index=True)
    condition_source_value = Column(String(50))
    condition_source_concept_id = Column(ForeignKey('concept.concept_id'))
    condition_status_source_value = Column(String(50))
    condition_status_concept_id = Column(ForeignKey('concept.concept_id'))

    condition_concept = relationship('Concept', primaryjoin='ConditionOccurrence.condition_concept_id == Concept.concept_id')
    condition_source_concept = relationship('Concept', primaryjoin='ConditionOccurrence.condition_source_concept_id == Concept.concept_id')
    condition_status_concept = relationship('Concept', primaryjoin='ConditionOccurrence.condition_status_concept_id == Concept.concept_id')
    condition_type_concept = relationship('Concept', primaryjoin='ConditionOccurrence.condition_type_concept_id == Concept.concept_id')
    person = relationship('Person', back_populates='condition_occurrence')
    provider = relationship('Provider')
    visit_occurrence = relationship('VisitOccurrence')

    def __repr__(self):
        return f"ConditionOccurrence(condition_occurrence_id='{self.condition_occurrence_id}', person_id='{self.person_id}', condition_concept_id='{self.condition_concept_id}')"


class DrugExposure(EhrBase):
    __tablename__ = 'drug_exposure'

    drug_exposure_id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    drug_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    drug_exposure_start_date = Column(Date, nullable=False)
    drug_exposure_start_datetime = Column(DateTime, nullable=False)
    drug_exposure_end_date = Column(Date, nullable=False)
    drug_exposure_end_datetime = Column(DateTime)
    verbatim_end_date = Column(Date)
    drug_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    stop_reason = Column(String(20))
    refills = Column(Integer)
    quantity = Column(Numeric)
    days_supply = Column(Integer)
    sig = Column(Text)
    route_concept_id = Column(ForeignKey('concept.concept_id'))
    lot_number = Column(String(50))
    provider_id = Column(ForeignKey('provider.provider_id'))
    visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'), index=True)
    drug_source_value = Column(String(50))
    drug_source_concept_id = Column(ForeignKey('concept.concept_id'))
    route_source_value = Column(String(50))
    dose_unit_source_value = Column(String(50))

    drug_concept = relationship('Concept', primaryjoin='DrugExposure.drug_concept_id == Concept.concept_id')
    drug_source_concept = relationship('Concept', primaryjoin='DrugExposure.drug_source_concept_id == Concept.concept_id')
    drug_type_concept = relationship('Concept', primaryjoin='DrugExposure.drug_type_concept_id == Concept.concept_id')
    person = relationship('Person', back_populates='drug_exposure')
    provider = relationship('Provider')
    route_concept = relationship('Concept', primaryjoin='DrugExposure.route_concept_id == Concept.concept_id')
    visit_occurrence = relationship('VisitOccurrence')

    def __repr__(self):
        return f"DrugExposure(drug_exposure_id='{self.drug_exposure_id}', person_id='{self.person_id}', drug_concept_id='{self.drug_concept_id}')"


class Measurement(EhrBase):
    __tablename__ = 'measurement'

    measurement_id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    measurement_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    measurement_date = Column(Date, nullable=False)
    measurement_datetime = Column(DateTime)
    measurement_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    operator_concept_id = Column(ForeignKey('concept.concept_id'))
    value_as_number = Column(Numeric)
    value_as_concept_id = Column(ForeignKey('concept.concept_id'))
    unit_concept_id = Column(ForeignKey('concept.concept_id'))
    range_low = Column(Numeric)
    range_high = Column(Numeric)
    provider_id = Column(ForeignKey('provider.provider_id'))
    visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'), index=True)
    measurement_source_value = Column(String(50))
    measurement_source_concept_id = Column(ForeignKey('concept.concept_id'))
    unit_source_value = Column(String(50))
    value_source_value = Column(String(50))


    measurement_concept = relationship('Concept', primaryjoin='Measurement.measurement_concept_id == Concept.concept_id')
    measurement_source_concept = relationship('Concept', primaryjoin='Measurement.measurement_source_concept_id == Concept.concept_id')
    measurement_type_concept = relationship('Concept', primaryjoin='Measurement.measurement_type_concept_id == Concept.concept_id')
    operator_concept = relationship('Concept', primaryjoin='Measurement.operator_concept_id == Concept.concept_id')
    person = relationship('Person', back_populates='measurement')
    provider = relationship('Provider')
    unit_concept = relationship('Concept', primaryjoin='Measurement.unit_concept_id == Concept.concept_id')
    value_as_concept = relationship('Concept', primaryjoin='Measurement.value_as_concept_id == Concept.concept_id')
    visit_occurrence = relationship('VisitOccurrence')

    def __repr__(self):
        return f"Measurement(measurement_id='{self.measurement_id}', person_id='{self.person_id}', measurement_concept_id='{self.measurement_concept_id}')"


class Observation(EhrBase):
    __tablename__ = 'observation'

    observation_id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    observation_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    observation_date = Column(Date, nullable=False)
    observation_datetime = Column(DateTime)
    observation_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    value_as_number = Column(Numeric)
    value_as_string = Column(String(60))
    value_as_concept_id = Column(ForeignKey('concept.concept_id'))
    qualifier_concept_id = Column(ForeignKey('concept.concept_id'))
    unit_concept_id = Column(ForeignKey('concept.concept_id'))
    provider_id = Column(ForeignKey('provider.provider_id'))
    visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'), index=True)
    observation_source_value = Column(String(50))
    observation_source_concept_id = Column(ForeignKey('concept.concept_id'))
    unit_source_value = Column(String(50))
    qualifier_source_value = Column(String(50))

    observation_concept = relationship('Concept', primaryjoin='Observation.observation_concept_id == Concept.concept_id')
    observation_source_concept = relationship('Concept', primaryjoin='Observation.observation_source_concept_id == Concept.concept_id')
    observation_type_concept = relationship('Concept', primaryjoin='Observation.observation_type_concept_id == Concept.concept_id')
    person = relationship('Person', back_populates='observation')
    provider = relationship('Provider')
    qualifier_concept = relationship('Concept', primaryjoin='Observation.qualifier_concept_id == Concept.concept_id')
    unit_concept = relationship('Concept', primaryjoin='Observation.unit_concept_id == Concept.concept_id')
    value_as_concept = relationship('Concept', primaryjoin='Observation.value_as_concept_id == Concept.concept_id')
    visit_occurrence = relationship('VisitOccurrence')

    def __repr__(self):
        return f"Observation(observation_id='{self.observation_id}', person_id='{self.person_id}', observation_concept_id='{self.observation_concept_id}')"


class ProcedureOccurrence(EhrBase):
    __tablename__ = 'procedure_occurrence'

    procedure_occurrence_id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    procedure_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    procedure_date = Column(Date, nullable=False)
    procedure_datetime = Column(DateTime, nullable=False)
    procedure_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    modifier_concept_id = Column(ForeignKey('concept.concept_id'))
    quantity = Column(Integer)
    provider_id = Column(ForeignKey('provider.provider_id'))
    visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'), index=True)
    procedure_source_value = Column(String(50))
    procedure_source_concept_id = Column(ForeignKey('concept.concept_id'))
    qualifier_source_value = Column(String(50))

    modifier_concept = relationship('Concept', primaryjoin='ProcedureOccurrence.modifier_concept_id == Concept.concept_id')
    person = relationship('Person', back_populates='procedure_occurrence')
    procedure_concept = relationship('Concept', primaryjoin='ProcedureOccurrence.procedure_concept_id == Concept.concept_id')
    procedure_source_concept = relationship('Concept', primaryjoin='ProcedureOccurrence.procedure_source_concept_id == Concept.concept_id')
    procedure_type_concept = relationship('Concept', primaryjoin='ProcedureOccurrence.procedure_type_concept_id == Concept.concept_id')
    provider = relationship('Provider')
    visit_occurrence = relationship('VisitOccurrence')

    def __repr__(self):
        return f"ProcedureOccurrence(procedure_occurrence_id='{self.procedure_occurrence_id}', person_id='{self.person_id}', procedure_concept_id='{self.procedure_concept_id}')"


class Concept(EhrBase):
    __tablename__ = 'concept'

    concept_id = Column(Integer, primary_key=True, unique=True)
    concept_name = Column(String(255), nullable=False)
    domain_id = Column(ForeignKey('domain.domain_id'), nullable=False, index=True)
    vocabulary_id = Column(ForeignKey('vocabulary.vocabulary_id'), nullable=False, index=True)
    concept_class_id = Column(ForeignKey('concept_class.concept_class_id'), nullable=False, index=True)
    standard_concept = Column(String(1))
    concept_code = Column(String(50), nullable=False, index=True)
    valid_start_date = Column(Date, nullable=False)
    valid_end_date = Column(Date, nullable=False)
    invalid_reason = Column(String(1))

    concept_class = relationship('ConceptClass', primaryjoin='Concept.concept_class_id == ConceptClass.concept_class_id')
    domain = relationship('Domain', primaryjoin='Concept.domain_id == Domain.domain_id')
    vocabulary = relationship('Vocabulary', primaryjoin='Concept.vocabulary_id == Vocabulary.vocabulary_id')

    def __repr__(self):
        return f"Concept(concept_id='{self.concept_id}', concept_name='{self.concept_name}', domain_id='{self.domain_id}')"


class Domain(EhrBase):
    __tablename__ = 'domain'

    domain_id = Column(String(20), primary_key=True, unique=True)
    domain_name = Column(String(255), nullable=False)
    domain_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)

    domain_concept = relationship('Concept', primaryjoin='Domain.domain_concept_id == Concept.concept_id')

    def __repr__(self):
        return f"Domain(domain_id='{self.domain_id}', domain_name='{self.domain_name}', domain_concept_id='{self.domain_concept_id}')"


t_cdm_source = Table(
    'cdm_source', ehr_metadata,
    Column('cdm_source_name', String(255), nullable=False),
    Column('cdm_source_abbreviation', String(25)),
    Column('cdm_holder', String(255)),
    Column('source_description', Text),
    Column('source_documentation_reference', String(255)),
    Column('cdm_etl_reference', String(255)),
    Column('source_release_date', Date),
    Column('cdm_release_date', Date),
    Column('cdm_version', String(10)),
    Column('vocabulary_version', String(20))
)


class AttributeDefinition(EhrBase):
    __tablename__ = 'attribute_definition'

    attribute_definition_id = Column(Integer, primary_key=True, index=True)
    attribute_name = Column(String(255), nullable=False)
    attribute_description = Column(Text)
    attribute_type_concept_id = Column(Integer, nullable=False)
    attribute_syntax = Column(Text)


class ConceptClass(EhrBase):
    __tablename__ = 'concept_class'

    concept_class_id = Column(String(20), primary_key=True, unique=True)
    concept_class_name = Column(String(255), nullable=False)
    concept_class_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)

    concept_class_concept = relationship('Concept', primaryjoin='ConceptClass.concept_class_concept_id == Concept.concept_id')


class Location(EhrBase):
    __tablename__ = 'location'

    location_id = Column(Integer, primary_key=True)
    address_1 = Column(String(50))
    address_2 = Column(String(50))
    city = Column(String(50))
    state = Column(String(2))
    zip = Column(String(9))
    county = Column(String(20))
    location_source_value = Column(String(50))


class Vocabulary(EhrBase):
    __tablename__ = 'vocabulary'

    vocabulary_id = Column(String(20), primary_key=True, unique=True)
    vocabulary_name = Column(String(255), nullable=False)
    vocabulary_reference = Column(String(255))
    vocabulary_version = Column(String(255))
    vocabulary_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)

    vocabulary_concept = relationship('Concept', primaryjoin='Vocabulary.vocabulary_concept_id == Concept.concept_id')


class CareSite(EhrBase):
    __tablename__ = 'care_site'

    care_site_id = Column(Integer, primary_key=True)
    care_site_name = Column(String(255))
    place_of_service_concept_id = Column(ForeignKey('concept.concept_id'))
    location_id = Column(ForeignKey('location.location_id'))
    care_site_source_value = Column(String(50))
    place_of_service_source_value = Column(String(50))

    location = relationship('Location')
    place_of_service_concept = relationship('Concept')


class CohortDefinition(EhrBase):
    __tablename__ = 'cohort_definition'

    cohort_definition_id = Column(Integer, primary_key=True, index=True)
    cohort_definition_name = Column(String(255), nullable=False)
    cohort_definition_description = Column(Text)
    definition_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    cohort_definition_syntax = Column(Text)
    subject_concept_id = Column(Integer, nullable=False)
    cohort_initiation_date = Column(Date)

    definition_type_concept = relationship('Concept')


class ConceptAncestor(EhrBase):
    __tablename__ = 'concept_ancestor'

    ancestor_concept_id = Column(ForeignKey('concept.concept_id'), primary_key=True, nullable=False, index=True)
    descendant_concept_id = Column(ForeignKey('concept.concept_id'), primary_key=True, nullable=False, index=True)
    min_levels_of_separation = Column(Integer, nullable=False)
    max_levels_of_separation = Column(Integer, nullable=False)

    ancestor_concept = relationship('Concept', primaryjoin='ConceptAncestor.ancestor_concept_id == Concept.concept_id')
    descendant_concept = relationship('Concept', primaryjoin='ConceptAncestor.descendant_concept_id == Concept.concept_id')


t_concept_synonym = Table(
    'concept_synonym', ehr_metadata,
    Column('concept_id', ForeignKey('concept.concept_id'), nullable=False, index=True),
    Column('concept_synonym_name', String(1000), nullable=False),
    Column('language_concept_id', Integer, nullable=False)
)


class DrugStrength(EhrBase):
    __tablename__ = 'drug_strength'

    drug_concept_id = Column(ForeignKey('concept.concept_id'), primary_key=True, nullable=False, index=True)
    ingredient_concept_id = Column(ForeignKey('concept.concept_id'), primary_key=True, nullable=False, index=True)
    amount_value = Column(Numeric)
    amount_unit_concept_id = Column(ForeignKey('concept.concept_id'))
    numerator_value = Column(Numeric)
    numerator_unit_concept_id = Column(ForeignKey('concept.concept_id'))
    denominator_value = Column(Numeric)
    denominator_unit_concept_id = Column(ForeignKey('concept.concept_id'))
    box_size = Column(Integer)
    valid_start_date = Column(Date, nullable=False)
    valid_end_date = Column(Date, nullable=False)
    invalid_reason = Column(String(1))

    amount_unit_concept = relationship('Concept', primaryjoin='DrugStrength.amount_unit_concept_id == Concept.concept_id')
    denominator_unit_concept = relationship('Concept', primaryjoin='DrugStrength.denominator_unit_concept_id == Concept.concept_id')
    drug_concept = relationship('Concept', primaryjoin='DrugStrength.drug_concept_id == Concept.concept_id')
    ingredient_concept = relationship('Concept', primaryjoin='DrugStrength.ingredient_concept_id == Concept.concept_id')
    numerator_unit_concept = relationship('Concept', primaryjoin='DrugStrength.numerator_unit_concept_id == Concept.concept_id')


t_fact_relationship = Table(
    'fact_relationship', ehr_metadata,
    Column('domain_concept_id_1', ForeignKey('concept.concept_id'), nullable=False, index=True),
    Column('fact_id_1', Integer, nullable=False),
    Column('domain_concept_id_2', ForeignKey('concept.concept_id'), nullable=False, index=True),
    Column('fact_id_2', Integer, nullable=False),
    Column('relationship_concept_id', ForeignKey('concept.concept_id'), nullable=False, index=True)
)


class Relationship(EhrBase):
    __tablename__ = 'relationship'

    relationship_id = Column(String(20), primary_key=True, unique=True)
    relationship_name = Column(String(255), nullable=False)
    is_hierarchical = Column(String(1), nullable=False)
    defines_ancestry = Column(String(1), nullable=False)
    reverse_relationship_id = Column(ForeignKey('relationship.relationship_id'), nullable=False)
    relationship_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)

    relationship_concept = relationship('Concept')
    reverse_relationship = relationship('Relationship', remote_side=[relationship_id])


class SourceToConceptMap(EhrBase):
    __tablename__ = 'source_to_concept_map'

    source_code = Column(String(50), primary_key=True, nullable=False, index=True)
    source_concept_id = Column(Integer, nullable=False)
    source_vocabulary_id = Column(ForeignKey('vocabulary.vocabulary_id'), primary_key=True, nullable=False, index=True)
    source_code_description = Column(String(255))
    target_concept_id = Column(ForeignKey('concept.concept_id'), primary_key=True, nullable=False, index=True)
    target_vocabulary_id = Column(ForeignKey('vocabulary.vocabulary_id'), nullable=False, index=True)
    valid_start_date = Column(Date, nullable=False)
    valid_end_date = Column(Date, primary_key=True, nullable=False)
    invalid_reason = Column(String(1))

    source_vocabulary = relationship('Vocabulary', primaryjoin='SourceToConceptMap.source_vocabulary_id == Vocabulary.vocabulary_id')
    target_concept = relationship('Concept')
    target_vocabulary = relationship('Vocabulary', primaryjoin='SourceToConceptMap.target_vocabulary_id == Vocabulary.vocabulary_id')


class Cohort(EhrBase):
    __tablename__ = 'cohort'

    cohort_definition_id = Column(ForeignKey('cohort_definition.cohort_definition_id'), primary_key=True, nullable=False, index=True)
    subject_id = Column(Integer, primary_key=True, nullable=False, index=True)
    cohort_start_date = Column(Date, primary_key=True, nullable=False)
    cohort_end_date = Column(Date, primary_key=True, nullable=False)

    cohort_definition = relationship('CohortDefinition')


class CohortAttribute(EhrBase):
    __tablename__ = 'cohort_attribute'

    cohort_definition_id = Column(ForeignKey('cohort_definition.cohort_definition_id'), primary_key=True, nullable=False, index=True)
    cohort_start_date = Column(Date, primary_key=True, nullable=False)
    cohort_end_date = Column(Date, primary_key=True, nullable=False)
    subject_id = Column(Integer, primary_key=True, nullable=False, index=True)
    attribute_definition_id = Column(ForeignKey('attribute_definition.attribute_definition_id'), primary_key=True, nullable=False)
    value_as_number = Column(Numeric)
    value_as_concept_id = Column(ForeignKey('concept.concept_id'))

    attribute_definition = relationship('AttributeDefinition')
    cohort_definition = relationship('CohortDefinition')
    value_as_concept = relationship('Concept')


class ConceptRelationship(EhrBase):
    __tablename__ = 'concept_relationship'

    concept_id_1 = Column(ForeignKey('concept.concept_id'), primary_key=True, nullable=False, index=True)
    concept_id_2 = Column(ForeignKey('concept.concept_id'), primary_key=True, nullable=False, index=True)
    relationship_id = Column(ForeignKey('relationship.relationship_id'), primary_key=True, nullable=False, index=True)
    valid_start_date = Column(Date, nullable=False)
    valid_end_date = Column(Date, nullable=False)
    invalid_reason = Column(String(1))

    concept = relationship('Concept', primaryjoin='ConceptRelationship.concept_id_1 == Concept.concept_id')
    concept1 = relationship('Concept', primaryjoin='ConceptRelationship.concept_id_2 == Concept.concept_id')
    relationship = relationship('Relationship')


class Provider(EhrBase):
    __tablename__ = 'provider'

    provider_id = Column(Integer, primary_key=True)
    provider_name = Column(String(255))
    npi = Column(String(20))
    dea = Column(String(20))
    specialty_concept_id = Column(ForeignKey('concept.concept_id'))
    care_site_id = Column(ForeignKey('care_site.care_site_id'))
    year_of_birth = Column(Integer)
    gender_concept_id = Column(ForeignKey('concept.concept_id'))
    provider_source_value = Column(String(50))
    specialty_source_value = Column(String(50))
    specialty_source_concept_id = Column(ForeignKey('concept.concept_id'))
    gender_source_value = Column(String(50))
    gender_source_concept_id = Column(ForeignKey('concept.concept_id'))

    care_site = relationship('CareSite')
    gender_concept = relationship('Concept', primaryjoin='Provider.gender_concept_id == Concept.concept_id')
    gender_source_concept = relationship('Concept', primaryjoin='Provider.gender_source_concept_id == Concept.concept_id')
    specialty_concept = relationship('Concept', primaryjoin='Provider.specialty_concept_id == Concept.concept_id')
    specialty_source_concept = relationship('Concept', primaryjoin='Provider.specialty_source_concept_id == Concept.concept_id')


class Death(Person):
    __tablename__ = 'death'

    person_id = Column(ForeignKey('person.person_id'), primary_key=True, index=True)
    death_date = Column(Date, nullable=False)
    death_datetime = Column(DateTime)
    death_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    cause_concept_id = Column(ForeignKey('concept.concept_id'))
    cause_source_value = Column(String(50))
    cause_source_concept_id = Column(ForeignKey('concept.concept_id'))

    cause_concept = relationship('Concept', primaryjoin='Death.cause_concept_id == Concept.concept_id')
    cause_source_concept = relationship('Concept', primaryjoin='Death.cause_source_concept_id == Concept.concept_id')
    death_type_concept = relationship('Concept', primaryjoin='Death.death_type_concept_id == Concept.concept_id')


class ConditionEra(EhrBase):
    __tablename__ = 'condition_era'

    condition_era_id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    condition_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    condition_era_start_date = Column(Date, nullable=False)
    condition_era_end_date = Column(Date, nullable=False)
    condition_occurrence_count = Column(Integer)

    condition_concept = relationship('Concept')
    person = relationship('Person')


class DoseEra(EhrBase):
    __tablename__ = 'dose_era'

    dose_era_id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    drug_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    unit_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    dose_value = Column(Numeric, nullable=False)
    dose_era_start_date = Column(Date, nullable=False)
    dose_era_end_date = Column(Date, nullable=False)

    drug_concept = relationship('Concept', primaryjoin='DoseEra.drug_concept_id == Concept.concept_id')
    person = relationship('Person')
    unit_concept = relationship('Concept', primaryjoin='DoseEra.unit_concept_id == Concept.concept_id')


class DrugEra(EhrBase):
    __tablename__ = 'drug_era'

    drug_era_id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    drug_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    drug_era_start_date = Column(Date, nullable=False)
    drug_era_end_date = Column(Date, nullable=False)
    drug_exposure_count = Column(Integer)
    gap_days = Column(Integer)

    drug_concept = relationship('Concept')
    person = relationship('Person')


class ObservationPeriod(EhrBase):
    __tablename__ = 'observation_period'

    observation_period_id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    observation_period_start_date = Column(Date, nullable=False)
    observation_period_end_date = Column(Date, nullable=False)
    period_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)

    period_type_concept = relationship('Concept')
    person = relationship('Person')


class PayerPlanPeriod(EhrBase):
    __tablename__ = 'payer_plan_period'

    payer_plan_period_id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    payer_plan_period_start_date = Column(Date, nullable=False)
    payer_plan_period_end_date = Column(Date, nullable=False)
    payer_source_value = Column(String(50))
    plan_source_value = Column(String(50))
    family_source_value = Column(String(50))

    person = relationship('Person')


class Speciman(EhrBase):
    __tablename__ = 'specimen'

    specimen_id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    specimen_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    specimen_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    specimen_date = Column(Date, nullable=False)
    specimen_datetime = Column(DateTime)
    quantity = Column(Numeric)
    unit_concept_id = Column(ForeignKey('concept.concept_id'))
    anatomic_site_concept_id = Column(ForeignKey('concept.concept_id'))
    disease_status_concept_id = Column(ForeignKey('concept.concept_id'))
    specimen_source_id = Column(String(50))
    specimen_source_value = Column(String(50))
    unit_source_value = Column(String(50))
    anatomic_site_source_value = Column(String(50))
    disease_status_source_value = Column(String(50))

    anatomic_site_concept = relationship('Concept', primaryjoin='Speciman.anatomic_site_concept_id == Concept.concept_id')
    disease_status_concept = relationship('Concept', primaryjoin='Speciman.disease_status_concept_id == Concept.concept_id')
    person = relationship('Person')
    specimen_concept = relationship('Concept', primaryjoin='Speciman.specimen_concept_id == Concept.concept_id')
    specimen_type_concept = relationship('Concept', primaryjoin='Speciman.specimen_type_concept_id == Concept.concept_id')
    unit_concept = relationship('Concept', primaryjoin='Speciman.unit_concept_id == Concept.concept_id')


class VisitOccurrence(EhrBase):
    __tablename__ = 'visit_occurrence'

    visit_occurrence_id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    visit_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    visit_start_date = Column(Date, nullable=False)
    visit_start_datetime = Column(DateTime)
    visit_end_date = Column(Date, nullable=False)
    visit_end_datetime = Column(DateTime)
    visit_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    provider_id = Column(ForeignKey('provider.provider_id'))
    care_site_id = Column(ForeignKey('care_site.care_site_id'))
    visit_source_value = Column(String(50))
    visit_source_concept_id = Column(ForeignKey('concept.concept_id'))
    admitting_source_concept_id = Column(ForeignKey('concept.concept_id'))
    admitting_source_value = Column(String(50))
    discharge_to_concept_id = Column(ForeignKey('concept.concept_id'))
    discharge_to_source_value = Column(String(50))
    preceding_visit_occurrence_id = Column(Integer)

    admitting_source_concept = relationship('Concept', primaryjoin='VisitOccurrence.admitting_source_concept_id == Concept.concept_id')
    care_site = relationship('CareSite')
    discharge_to_concept = relationship('Concept', primaryjoin='VisitOccurrence.discharge_to_concept_id == Concept.concept_id')
    person = relationship('Person')
    provider = relationship('Provider')
    visit_concept = relationship('Concept', primaryjoin='VisitOccurrence.visit_concept_id == Concept.concept_id')
    visit_source_concept = relationship('Concept', primaryjoin='VisitOccurrence.visit_source_concept_id == Concept.concept_id')
    visit_type_concept = relationship('Concept', primaryjoin='VisitOccurrence.visit_type_concept_id == Concept.concept_id')


class Cost(EhrBase):
    __tablename__ = 'cost'

    cost_id = Column(Integer, primary_key=True)
    cost_event_id = Column(Integer, nullable=False)
    cost_domain_id = Column(String(20), nullable=False)
    cost_type_concept_id = Column(Integer, nullable=False)
    currency_concept_id = Column(ForeignKey('concept.concept_id'))
    total_charge = Column(Numeric)
    total_cost = Column(Numeric)
    total_paid = Column(Numeric)
    paid_by_payer = Column(Numeric)
    paid_by_patient = Column(Numeric)
    paid_patient_copay = Column(Numeric)
    paid_patient_coinsurance = Column(Numeric)
    paid_patient_deductible = Column(Numeric)
    paid_by_primary = Column(Numeric)
    paid_ingredient_cost = Column(Numeric)
    paid_dispensing_fee = Column(Numeric)
    payer_plan_period_id = Column(ForeignKey('payer_plan_period.payer_plan_period_id'))
    amount_allowed = Column(Numeric)
    revenue_code_concept_id = Column(Integer)
    reveue_code_source_value = Column(String(50))
    drg_concept_id = Column(ForeignKey('concept.concept_id'))
    drg_source_value = Column(String(3))

    currency_concept = relationship('Concept', primaryjoin='Cost.currency_concept_id == Concept.concept_id')
    drg_concept = relationship('Concept', primaryjoin='Cost.drg_concept_id == Concept.concept_id')
    payer_plan_period = relationship('PayerPlanPeriod')


class DeviceExposure(EhrBase):
    __tablename__ = 'device_exposure'

    device_exposure_id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    device_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    device_exposure_start_date = Column(Date, nullable=False)
    device_exposure_start_datetime = Column(DateTime, nullable=False)
    device_exposure_end_date = Column(Date)
    device_exposure_end_datetime = Column(DateTime)
    device_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    unique_device_id = Column(String(50))
    quantity = Column(Integer)
    provider_id = Column(ForeignKey('provider.provider_id'))
    visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'), index=True)
    device_source_value = Column(String(100))
    device_source_concept_id = Column(ForeignKey('concept.concept_id'))

    device_concept = relationship('Concept', primaryjoin='DeviceExposure.device_concept_id == Concept.concept_id')
    device_source_concept = relationship('Concept', primaryjoin='DeviceExposure.device_source_concept_id == Concept.concept_id')
    device_type_concept = relationship('Concept', primaryjoin='DeviceExposure.device_type_concept_id == Concept.concept_id')
    person = relationship('Person')
    provider = relationship('Provider')
    visit_occurrence = relationship('VisitOccurrence')


class Note(EhrBase):
    __tablename__ = 'note'

    note_id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    note_date = Column(Date, nullable=False)
    note_datetime = Column(DateTime)
    note_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    note_class_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    note_title = Column(String(250))
    note_text = Column(Text, nullable=False)
    encoding_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    language_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    provider_id = Column(ForeignKey('provider.provider_id'))
    visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'), index=True)
    note_source_value = Column(String(50))

    encoding_concept = relationship('Concept', primaryjoin='Note.encoding_concept_id == Concept.concept_id')
    language_concept = relationship('Concept', primaryjoin='Note.language_concept_id == Concept.concept_id')
    note_class_concept = relationship('Concept', primaryjoin='Note.note_class_concept_id == Concept.concept_id')
    note_type_concept = relationship('Concept', primaryjoin='Note.note_type_concept_id == Concept.concept_id')
    person = relationship('Person')
    provider = relationship('Provider')
    visit_occurrence = relationship('VisitOccurrence')


class NoteNlp(EhrBase):
    __tablename__ = 'note_nlp'

    note_nlp_id = Column(BigInteger, primary_key=True)
    note_id = Column(ForeignKey('note.note_id'), nullable=False, index=True)
    section_concept_id = Column(ForeignKey('concept.concept_id'))
    snippet = Column(String(250))
    offset = Column(String(250))
    lexical_variant = Column(String(250), nullable=False)
    note_nlp_concept_id = Column(ForeignKey('concept.concept_id'), index=True)
    note_nlp_source_concept_id = Column(Integer)
    nlp_system = Column(String(250))
    nlp_date = Column(Date, nullable=False)
    nlp_datetime = Column(DateTime)
    term_exists = Column(String(1))
    term_temporal = Column(String(50))
    term_modifiers = Column(String(2000))

    note = relationship('Note')
    note_nlp_concept = relationship('Concept', primaryjoin='NoteNlp.note_nlp_concept_id == Concept.concept_id')
    section_concept = relationship('Concept', primaryjoin='NoteNlp.section_concept_id == Concept.concept_id')


################################################################
#                  END of DB tables for EHR DB                 #
################################################################