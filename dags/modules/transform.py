from datetime import datetime
import hashlib


def generate_id(row):
    # Crear una cadena que represente los datos de la fila
    data_string = f"{row['symbol']}-{row['date']}-{row['opening_price']}-{row['closing_price']}-{row['category']}-{row['description']}"
    
    # Generar un hash MD5 de la cadena
    return hashlib.md5(data_string.encode()).hexdigest()

def transform_data(df):

    try:
        # Renombrar columnas para que coincidan con los nombres esperados
        df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume', 'symbol', 'category', 'description']
            
        # Convertir 'datetime' a solo fecha
        df['date'] = df['datetime'].apply(lambda x: x.split('T')[0])
            
        # Añadir columnas adicionales
        df['ingest_date'] = datetime.now().strftime('%Y-%m-%d')  # Fecha de ingreso del registro
            
        # Verificar que las columnas esperadas estén presentes
        if 'open' not in df.columns or 'close' not in df.columns:
            raise KeyError("Las columnas 'open' o 'close' están ausentes en los datos")
            
        # Renombrar columnas finales
        df.rename(columns={'open': 'opening_price', 'close': 'closing_price'}, inplace=True) # Por problemas de palabras reservadas
            
        # Generar ID basado en los datos de la fila
        df['id'] = df.apply(generate_id, axis=1)
            
        # Selección y reordenamiento de columnas
        df = df[['id', 'symbol', 'date', 'opening_price', 'closing_price', 'category', 'description', 'ingest_date']]

        # Imprime los primeros registros del DataFrame resultante, solo para visualizar
        print("Datos transformados:\n")
        print(df.head())

        # Guarda los datos transformados en un archivo CSV en la carpeta temporal
        df.to_csv('/tmp/transformed_data.csv', index=False)
    
        print("Datos correctamente transformados!")

    # Maneja cualquier excepción que pueda ocurrir durante la transformacion de datos y muestra un mensaje de error    
    except Exception as e:
        print(f"Error en la transformación de datos: {e}")
        return None
        
