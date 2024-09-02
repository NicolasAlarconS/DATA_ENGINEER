import sys
import os

# Añade el directorio 'dags/modules' al PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from modules import extract, transform, load 

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

    # Tarea de extracción
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract.extract_data,
        dag=dag
    )

    # Tarea de transformación
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=lambda: transform.transform_data(pd.read_csv('/tmp/extracted_data.csv')),
        dag=dag
    )

    # Tarea de carga
    load_task = PythonOperator(
        task_id='load_data',
        python_callable=lambda: load.load_data(pd.read_csv('/tmp/transformed_data.csv')),
        dag=dag
    )

    # Definir dependencias
    extract_task >> transform_task >> load_task

