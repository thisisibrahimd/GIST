import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
# Format: postgresql://user:password@hostname:port/database
GIST_EHR_CONN_STR = os.environ.get('GIST_EHR_CONN_STR')
GIST_CRIT_CONN_STR = os.environ.get('GIST_CRIT_CONN_STR')