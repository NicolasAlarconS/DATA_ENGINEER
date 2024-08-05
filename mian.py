import requests
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

REDSHIFT_USER = os.getenv('REDSHIFT_USER')
REDSHIFT_PASSWORD = os.getenv('REDSHIFT_PASSWORD')
REDSHIFT_HOST = os.getenv('REDSHIFT_HOST')
REDSHIFT_PORT = os.getenv('REDSHIFT_PORT')
REDSHIFT_DB = os.getenv('REDSHIFT_DB')
REDSHIFT_SCHEMA = os.getenv('REDSHIFT_SCHEMA')
TWELVE_DATA_API_KEY = os.getenv('TWELVE_DATA_API_KEY')

# Conexión a Redshift
def connect_redshift():
    try:
        conn = psycopg2.connect(
            dbname=REDSHIFT_DB,
            user=REDSHIFT_USER,
            password=REDSHIFT_PASSWORD,
            host=REDSHIFT_HOST,
            port=REDSHIFT_PORT
        )
        print("Conexión a Redshift exitosa!")
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to Redshift: {e}")
        raise

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
            print(f"No data found for symbol: {symbol}")
            return None

        values = data['values'][:10]  # Obtener los últimos 10 registros
        return values
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Manejo de los datos
def transform_data(symbol, description, category, data):
    try:
        # Crear DataFrame con los datos
        df = pd.DataFrame(data)
        
        # Renombrar columnas
        df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
        
        # Convertir 'datetime' a solo fecha
        df['date'] = df['datetime'].apply(lambda x: x.split('T')[0])
        
        # Añadir columnas adicionales
        df['symbol'] = symbol
        df['category'] = category
        df['description'] = description
        df['ingest_date'] = datetime.now().strftime('%Y-%m-%d')  # Fecha de ingreso del registro
        
        # Selección de columnas finales
        df = df[['symbol', 'date', 'open', 'close', 'category', 'description', 'ingest_date']]
        df.columns = ['symbol', 'date', 'opening_price', 'closing_price', 'category', 'description', 'ingest_date']
        
        return df
    except Exception as e:
        print(f"Error transforming data for symbol: {symbol}: {e}")
        return None

# Carga de datos a Redshift
def load_data(df):
    if df is None or df.empty:
        print("No data to load.")
        return

    conn = connect_redshift()
    try:
        with conn.cursor() as cursor:
            # Crear la tabla stock_data en el esquema especificado
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {REDSHIFT_SCHEMA}.stock_data (
                symbol VARCHAR(10),
                date DATE,
                opening_price DOUBLE PRECISION,
                closing_price DOUBLE PRECISION,
                category VARCHAR(20),
                description VARCHAR(50),
                ingest_date DATE
            );
            """)
            print("Tabla en Redshift lista!")

            # Preparar datos para inserción en bloque
            block_size = 100  # Tamaño del bloque
            for start in range(0, len(df), block_size):
                end = start + block_size
                block_df = df.iloc[start:end]
                rows_to_insert = [
                    (row['symbol'], row['date'], row['opening_price'], row['closing_price'], row['category'], row['description'], row['ingest_date'])
                    for _, row in block_df.iterrows()
                ]
                
                # Inserción en bloque
                insert_query = f"""
                INSERT INTO {REDSHIFT_SCHEMA}.stock_data (symbol, date, opening_price, closing_price, category, description, ingest_date)
                VALUES %s
                """
                execute_values(cursor, insert_query, rows_to_insert)
                
                conn.commit()
                print(f"Se han agregado un bloque de {len(rows_to_insert)} registros a Redshift.")

    except psycopg2.Error as e:
        print(f"Error loading data into Redshift: {e}")
    finally:
        conn.close()

# Datos a extraer
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

# Función ETL
def etl():
    all_data = pd.DataFrame()
    for symbol, (description, category) in stocks.items():
        print(f"Processing {symbol}...")
        data = extract_data(symbol)
        if data is not None:
            transformed_data = transform_data(symbol, description, category, data)
            if transformed_data is not None:
                all_data = pd.concat([all_data, transformed_data], ignore_index=True)
            print("Transformación de datos exitosa!")
    if not all_data.empty:
        load_data(all_data)

if __name__ == "__main__":
    etl()


