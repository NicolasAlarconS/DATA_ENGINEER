import pandas as pd
from .api import extract_data
from .transform import transform_data
from .database import load_data

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
    all_data = pd.DataFrame() # Df que almacenara toda la data
    for symbol, (description, category) in stocks.items():
        print(f"Extrayendo.... {symbol}...")
        data = extract_data(symbol)
        if data is not None:
            transformed_data = transform_data(symbol, description, category, data)
            if transformed_data is not None:
                all_data = pd.concat([all_data, transformed_data], ignore_index=True)
            print("Transformación de datos exitosa!")
    if not all_data.empty:
        load_data(all_data)
