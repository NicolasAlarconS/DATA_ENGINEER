import psycopg2
from config import REDSHIFT_USER, REDSHIFT_PASSWORD, REDSHIFT_HOST, REDSHIFT_PORT, REDSHIFT_DB


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
        print(f"Error en la conexión a Redshift: {e}")
        raise