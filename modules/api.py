import requests
from .config import TWELVE_DATA_API_KEY

# Extracción de datos de Twelve Data
def extract_data(symbol):
    try:
        url = 'https://api.twelvedata.com/time_series'
        params = {
            'symbol': symbol,
            'interval': '1day',
            'apikey': TWELVE_DATA_API_KEY,
            'timezone': 'America/New_York'
        }
        response = requests.get(url, params=params)
        data = response.json()

        if 'values' not in data or not data['values']:
            print(f"No se encontraron datos de: {symbol}")
            return None

        values = data['values'][:10]  # Obtener los últimos 10 registros
        print(f"Datos recibidos para {symbol}") # Mostrar los primeros datos para verificar
        return values
    except Exception as e:
        print(f"Error de extraccion de datos de {symbol}: {e}")
        return None
