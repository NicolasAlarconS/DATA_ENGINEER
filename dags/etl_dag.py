from modules.extract import extract_data
from modules.transform import transform_data
from modules.load import load_data
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
    'etl_pipeline_dag',
    default_args=default_args,
    description='Pipeline de ETL para datos financieros',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # Definir las tareas
    task_extract = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    task_transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,  
    )

    task_load = PythonOperator(
        task_id='load_data',
        python_callable=load_data,    
    )

    # Definir las dependencias
    task_extract >> task_transform >> task_load

