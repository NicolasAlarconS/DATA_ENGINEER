import os
from dotenv import load_dotenv

# Ruta al archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '../config/.env')

# Cargar variables de entorno
load_dotenv(dotenv_path)

REDSHIFT_USER = os.getenv('REDSHIFT_USER')
REDSHIFT_PASSWORD = os.getenv('REDSHIFT_PASSWORD')
REDSHIFT_HOST = os.getenv('REDSHIFT_HOST')
REDSHIFT_PORT = os.getenv('REDSHIFT_PORT')
REDSHIFT_DB = os.getenv('REDSHIFT_DB')
REDSHIFT_SCHEMA = os.getenv('REDSHIFT_SCHEMA')
TWELVE_DATA_API_KEY = os.getenv('TWELVE_DATA_API_KEY')
