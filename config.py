import os
from datetime import timedelta
import logging

# Phone Info endpoint settings:
NTRUBKU_HOST = "https://www.neberitrubku.ru/nomer-telefona"

# Actuality settings:
REPOSITORY_ACTUALITY_DELTA = timedelta(days=7)
REVIEW_ACTUALITY_DELTA = timedelta(days=30)

# Logging settings:
WRITE_LOG_TO_FILE = False
LOG_FILENAME = "log.txt"
LOG_LEVEL = logging.INFO

# Auth settings:
FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', "dummy-flask-key")
MOBILE_API_KEY = os.environ.get("MOBILE_API_KEY", "dummy-api-key")


def get_postgres_uri():
    localhost_db_string = f"postgresql://postgres:qwerty@localhost:5432/phones"
    return os.environ.get("PG_DATABASE_URL", localhost_db_string)


# def get_api_url():
#     host = os.environ.get("API_HOST", "localhost")
#     port = 5000 if host == "localhost" else 80
#     return f"https://{host}:{port}"
