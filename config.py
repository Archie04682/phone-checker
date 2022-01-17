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
    localhost_db_string = f"postgresql://postgres:qwerty@localhost:5432/phones"
    return os.environ.get("PG_DATABASE_URL", localhost_db_string)


# def get_api_url():
#     host = os.environ.get("API_HOST", "localhost")
#     port = 5005 if host == "localhost" else 80
#     return f"http://{host}:{port}"
