import sys
import os

# Añade el directorio 'dags/modules' al PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.main import etl
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


# Argumentos por defecto para el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 30),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Definición del DAG usando `with DAG as`
with DAG(
    '0_ETL_DAG_NICOLAS_ALARCON',
    default_args=default_args,
    description='ETL para datos financieros',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # Definir las tareas
    task_extract = PythonOperator(
        task_id='ETL',
        python_callable=etl,
    )

    task_extract 
