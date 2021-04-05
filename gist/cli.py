import os
import logging
import click
import os
from gist.core import get_gist_score
from gist.repo import CritRepo, EhrRepo
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)

@click.command()
@click.option('-d', '--debug', is_flag=True, envvar="GIST_DEBUG", help="Show debug output. Automatically pulls from environment")
@click.option('-ehr', '--ehr-conn-str', required=True, envvar="GIST_EHR_CONN_STR", help="EHR db connection string. Automatically pulls from current environment")
@click.option('-crit', '--crit-conn-str', required=True, envvar="GIST_CRIT_CONN_STR", help="CRIT db connection string. Automatically pulls from current environment")
@click.option('-t', '--trial_id', 'trial_ids', required=True, multiple=True, envvar="GIST_TRIAL_IDS", help="Trial ID(s)")
def cli(debug, trial_ids, ehr_conn_str, crit_conn_str):
    """OMOP CDM Based Automatic Clinical Trial Generalizability Assessment Framework."""

    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    logger.info(f"logging level set to {'debug' if debug else 'info'}")

    ehr_repo = EhrRepo(ehr_conn_str)
    crit_repo = CritRepo(crit_conn_str)

    ehr = ehr_repo.get_ehr()

    criteria_by_trial_ids = []
    for trial_id in trial_ids:
        criteria_by_trial_id = {
            'trial_id': trial_id,
            'criteria': crit_repo.get_criteria_by_trial_id(trial_id)
        }
        criteria_by_trial_ids.append(criteria_by_trial_id)

    gist_scores = []
    for criteria_by_trial_id in criteria_by_trial_ids:
        gist_score = get_gist_score(criteria_by_trial_id['trial_id'], criteria_by_trial_id['criteria'], ehr)
        gist_scores.append(gist_score)
    logger.info(gist_scores)

if __name__ == '__main__':
    cli(auto_envvar_prefix='GIST')