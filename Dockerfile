FROM apache/airflow:slim-latest-python3.11

# Copiar los archivos necesarios
COPY dependencies/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

USER root

RUN apt-get update && apt-get install -y \
    wget

# Da permisos de ejecución al script de inicialización
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Configura la variable PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/usr/src/app/modules"

USER airflow

ENTRYPOINT ["/bin/bash","/start.sh"]

# Exponemos el puerto 8080 para acceder al servidor web de Airflow
EXPOSE 8080
