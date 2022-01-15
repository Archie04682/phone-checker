import os
from datetime import timedelta
import logging

# Phone Info endpoint settings:
NTRUBKU_HOST = "https://www.neberitrubku.ru/nomer-telefona"

# Cache settings:
ACTUALITY_DELTA = timedelta(days=7)

# Logging settings:
WRITE_LOG_TO_FILE = False
LOG_FILENAME = "log.txt"
LOG_LEVEL = logging.INFO


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = 54321 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "abc123")
    user, db_name = "allocation", "allocation"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


# def get_api_url():
#     host = os.environ.get("API_HOST", "localhost")
#     port = 5005 if host == "localhost" else 80
#     return f"http://{host}:{port}"
