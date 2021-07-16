import os
from dotenv import load_dotenv

load_dotenv()
ENVIRONMENT = os.getenv('ENVIRONMENT')


GEOCODING_KEY = os.getenv('GEOCODING_KEY')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DBNAME = os.getenv('DB_DBNAME')

DB_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DBNAME}"
