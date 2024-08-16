
FROM apache/airflow:2.9.2

USER root

# Crear directorios necesarios
RUN mkdir -p /opt/airflow/dags /opt/airflow/modules

# Copiar los archivos necesarios
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copiar los DAGs y módulos
COPY dags /opt/airflow/dags
COPY modules /opt/airflow/modules

USER airflow

# Da permisos de ejecución al script de inicialización
RUN chmod +x init_airflow.sh

# Exponemos el puerto 8080 para acceder al servidor web de Airflow
EXPOSE 8080

# Comando por defecto
CMD ["webserver"]
