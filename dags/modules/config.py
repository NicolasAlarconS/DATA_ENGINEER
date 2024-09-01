# Variables de entorno:
REDSHIFT_USER = 'nicolas_alarcon_k_coderhouse'
REDSHIFT_PASSWORD = 'nf32F7968i'
REDSHIFT_HOST = 'data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com'
REDSHIFT_PORT = '5439'
REDSHIFT_DB = 'data-engineer-database'
REDSHIFT_SCHEMA = 'nicolas_alarcon_k_coderhouse'
TWELVE_DATA_API_KEY = 'f1b1d80a8e4c4e9fb0bf76f14817f94f' 

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
