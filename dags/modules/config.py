import os
from dotenv import load_dotenv

# Ruta al archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')

# Cargar variables de entorno
load_dotenv(dotenv_path)

REDSHIFT_USER = os.getenv('REDSHIFT_USER')
REDSHIFT_PASSWORD = os.getenv('REDSHIFT_PASSWORD')
REDSHIFT_HOST = os.getenv('REDSHIFT_HOST')
REDSHIFT_PORT = os.getenv('REDSHIFT_PORT')
REDSHIFT_DB = os.getenv('REDSHIFT_DB')
REDSHIFT_SCHEMA = os.getenv('REDSHIFT_SCHEMA')
TWELVE_DATA_API_KEY = os.getenv('TWELVE_DATA_API_KEY')

# URL de la api
URL = 'https://api.twelvedata.com/time_series'

# Valores a extraer
stocks = {
    'AAPL': ('Apple Inc.', 'tech'),
    'MSFT': ('Microsoft Corp.', 'tech'),
    'GOOGL': ('Alphabet Inc. (Google)', 'tech'),
    'AMD': ('Advanced Micro Devices Inc.', 'tech'),
    'XLB': ('Materials Select Sector SPDR Fund', 'etf'),
    'WMT': ('Walmart Inc.', 'consumer'),
    'PFE': ('Pfizer Inc.', 'healthcare'),
    'VZ': ('Verizon Communications Inc.', 'communications'),
}
