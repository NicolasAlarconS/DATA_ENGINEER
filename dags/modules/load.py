import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from redshift_conn import connect_redshift
from config import REDSHIFT_SCHEMA


# Carga de datos a Redshift
def load_data(df):

    #ti = kwargs['ti']

    # Obtener el DataFrame JSON de la tarea anterior
    #transformed_data_json = ti.xcom_pull(task_ids='transform_data', key='transformed_data')
    
    #if true solo por futura mudificacion
    if True:
        #df = pd.read_json(transformed_data_json)
    
        # Conexion a Redshift
        conn = connect_redshift()

        try:
            with conn.cursor() as cursor:

                # Crear la tabla stock_data en el esquema especificado
                cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {REDSHIFT_SCHEMA}.stock_data (
                    id VARCHAR(64) PRIMARY KEY,
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
                    
                    # Obtener IDs existentes en la tabla
                    cursor.execute(f"SELECT id FROM {REDSHIFT_SCHEMA}.stock_data;")
                    existing_ids = {row[0] for row in cursor.fetchall()}
                    
                    # Filtrar datos no duplicados basados en el ID
                    new_rows = block_df[~block_df['id'].isin(existing_ids)]
                    
                    if new_rows.empty:
                        print(f"No se agregaron registros nuevos.")
                        continue
                    
                    # Filas a insertar
                    rows_to_insert = list(new_rows.to_records(index=False))
                    
                    # Insercion en bloque
                    insert_query = f"""
                    INSERT INTO {REDSHIFT_SCHEMA}.stock_data (id, symbol, date, opening_price, closing_price, category, description, ingest_date)
                    VALUES %s
                    """
                    execute_values(cursor, insert_query, rows_to_insert)
                    
                    conn.commit()
                    print(f"Se ha agregado un bloque de {len(rows_to_insert)} registros a Redshift.")

        except psycopg2.Error as e:
            print(f"Error cargando datos a Redshift: {e}")
        finally:
            conn.close()

    else:
        raise ValueError("No se encontraron datos transformados.")