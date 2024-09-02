import pandas as pd
import requests
from config import stocks, TWELVE_DATA_API_KEY, URL


def extract_data():
    df = pd.DataFrame()
    for symbol, (description, category) in stocks.items():
        try:
            params = {
                'symbol': symbol,
                'interval': '1day',
                'apikey': TWELVE_DATA_API_KEY,
                'timezone': 'America/New_York'
            }
            response = requests.get(URL, params=params)
            data = response.json()
            if 'values' not in data or not data['values']:
                print(f"No se encontraron datos de: {symbol}")
                continue
            values = data['values'][:10]
            extracted_data = pd.DataFrame(values)
            extracted_data['symbol'] = symbol
            extracted_data['category'] = category
            extracted_data['description'] = description
            df = pd.concat([df, extracted_data], ignore_index=True)
        except Exception as e:
            print(f"Error de extracción de datos de {symbol}: {e}")
    df.to_csv('/tmp/extracted_data.csv', index=False)


