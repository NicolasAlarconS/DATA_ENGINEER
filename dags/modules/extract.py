import requests
import pandas as pd
from config import stocks, TWELVE_DATA_API_KEY, URL


# Extracción de datos de Twelve Data
def extract_data():
    df = pd.DataFrame()
    for symbol, (description, category) in stocks.items():
        try:

            url = URL
            
            params = {
                'symbol': symbol,
                'interval': '1day',
                'apikey': TWELVE_DATA_API_KEY,
                'timezone': 'America/New_York'
            }
            response = requests.get(url, params=params)
            data = response.json()

            # Asegurar que el item a extraer exista o tenga datos
            if 'values' not in data or not data['values']:
                print(f"No se encontraron datos de: {symbol}")
                continue  # Continuar con el siguiente símbolo

            # Al ser demasiados datos solo sseleccionamos los mas recientes    
            values = data['values'][:10]  # Obtener los últimos 10 registros
            print(f"Datos recibidos para {symbol}") 

            # Se agrega informacion adicional necesaria
            extracted_data = pd.DataFrame(values) 
            extracted_data['symbol'] = symbol
            extracted_data['category'] = category
            extracted_data['description'] = description

            # Concatena toda la extraccion en un solo dataframe
            df = pd.concat([df, extracted_data], ignore_index=True)

        except Exception as e:
            print(f"Error de extraccion de datos de {symbol}: {e}")

    # Convertir el DataFrame a JSON para pasar por XCom
    #df_json = df.to_json()

    # Guardar el DataFrame JSON en XCom
    #kwargs['ti'].xcom_push(key='extracted_data', value=df_json)

    return df

