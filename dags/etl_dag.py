import sys
import os

# Añade el directorio 'dags/modules' al PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from modules import extract, transform, load, email_notification


# Argumentos por defecto para el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'on_failure_callback': email_notification.handle_dag_status,
    'on_success_callback': email_notification.handle_dag_status,
}

# Definición del DAG
with DAG(
    'ETL_NICOLAS_ALARCON',
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

    # Sensor para verificar la existencia del archivo csv extraido
    extract_file_sensor = FileSensor(
        task_id='extract_file_sensor',
        fs_conn_id='fs_default',
        filepath='/tmp/extracted_data.csv',
        poke_interval=30,  # Tiempo en segundos entre comprobaciones
        timeout=600,  # Tiempo máximo en segundos para esperar el archivo
        mode='poke',  
        dag=dag
    )

    # Sensor para verificar la existencia del archivo csv transformado
    transform_file_sensor = FileSensor(
        task_id='transform_file_sensor',
        fs_conn_id='fs_default',
        filepath='/tmp/transformed_data.csv',
        poke_interval=30,  # Tiempo en segundos entre comprobaciones
        timeout=600,  # Tiempo máximo en segundos para esperar el archivo
        mode='poke',  
        dag=dag
    )

    # Eliminar archivos temporales del directorio /tmp
    cleanup_tmp_files = BashOperator(
    task_id='cleanup_tmp_files',
    bash_command='rm -rf /tmp/*',  # Elimina todos los archivos y carpetas en /tmp
    dag=dag,
    )

    # Definir dependencias
    extract_task >> extract_file_sensor >> transform_task >> transform_file_sensor >> load_task >> cleanup_tmp_files

