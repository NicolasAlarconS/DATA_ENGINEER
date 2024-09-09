import pandas as pd
import requests
from config import stocks, TWELVE_DATA_API_KEY, URL


def extract_data():
    # Inicializa un DataFrame vacío para almacenar los datos extraídos de cada símbolo
    df = pd.DataFrame()
    
    # Itera sobre un diccionario 'stocks', donde cada clave es el símbolo y cada valor es una tupla (descripción, categoría)
    for symbol, (description, category) in stocks.items():
        try:
            # Crea los parámetros de consulta para la API de Twelve Data, incluyendo el símbolo, intervalo, clave de API y zona horaria
            params = {
                'symbol': symbol,
                'interval': '1day',  # Datos diarios
                'apikey': TWELVE_DATA_API_KEY,  # Clave de API que debe estar definida
                'timezone': 'America/New_York'  # Define la zona horaria
            }
            
            # Realiza una solicitud GET a la API usando la URL y los parámetros definidos
            response = requests.get(URL, params=params)
            
            # Convierte la respuesta a formato JSON
            data = response.json()
            
            # Verifica si el campo 'values' no está vacío y existe en los datos. Si no hay datos, imprime un mensaje y continúa con el siguiente símbolo
            if 'values' not in data or not data['values']:
                print(f"No se encontraron datos de: {symbol}")
                continue
            
            # Extrae los primeros 10 registros de los valores retornados por la API para no hacer tan pesado este proyecto
            values = data['values'][:10]
            
            # Convierte los valores extraídos en un DataFrame
            extracted_data = pd.DataFrame(values)
            
            # Añade columnas adicionales al DataFrame: 'symbol', 'category' y 'description'
            extracted_data['symbol'] = symbol  # Agrega el símbolo a cada fila
            extracted_data['category'] = category  # Añade la categoría de cada símbolo
            extracted_data['description'] = description  # Añade la descripción del símbolo
            
            # Combina el DataFrame actual con los datos ya extraídos, ignorando los índices para evitar duplicados
            df = pd.concat([df, extracted_data], ignore_index=True)
        
        # Maneja cualquier excepción que pueda ocurrir durante la extracción de datos y muestra un mensaje de error
        except Exception as e:
            print(f"Error de extracción de datos de {symbol}: {e}")
    
    # Imprime los primeros registros del DataFrame resultante, solo para visualizar 
    print("Datos extraídos:\n")
    print(df.head())
    
    # Guarda los datos extraídos en un archivo CSV en la carpeta temporal
    df.to_csv('/tmp/extracted_data.csv', index=False)



