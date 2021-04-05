import logging
from sqlalchemy import create_engine, select, func, funcfilter
from sqlalchemy.orm import sessionmaker, lazyload, joinedload, subqueryload
from gist.entities import EligibilityCriterion, Person, ConditionOccurrence, DrugExposure, Measurement, Observation, ProcedureOccurrence

class Repo:

    def __init__(self, conn_str):
        self.conn_str = conn_str
        self.engine = create_engine(self.conn_str)
        self.session = sessionmaker(self.engine)


class CritRepo(Repo):

    def get_all_trial_ids(self):
        stmt = (
            select(EligibilityCriterion.nct_id)
        )
        logging.debug(f"query for get_all_trial_ids: {stmt}")
        with self.session() as session:
            trial_ids = session.execute(stmt).scalars().unique()
        return trial_ids

    def get_criteria_by_trial_id(self, trial_id):
        stmt = (
            select(EligibilityCriterion)
            .filter(EligibilityCriterion.nct_id == trial_id)
        )
        logging.debug(f"query for get_criteria_by_trial_id: {stmt}")
        with self.session() as session:
            trials = session.execute(stmt).scalars().all()
        return trials


class EhrRepo(Repo):

    def get_ehr(self):
        stmt = (
            select(Person)
            .options(subqueryload(Person.condition_occurrence))
            .options(subqueryload(Person.drug_exposure))
            .options(subqueryload(Person.procedure_occurrence))
            .options(subqueryload(Person.observation))
            .options(subqueryload(Person.measurement))
        )
        logging.debug(f"query for get_ehr: {stmt}")
        with self.session() as session:
            ehr = session.execute(stmt).scalars().unique().all()
        return ehr
