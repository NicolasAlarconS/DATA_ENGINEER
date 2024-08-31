#!/bin/bash

# Inicializa la base de datos de Airflow
airflow db migrate

# Crea un usuario administrador si no existe (opcional)
airflow users create \
    --username admin \
    --password admin \
    --firstname admin \
    --lastname admin \
    --role admin \
    --email admin@example.com

# Arranca el scheduler y el webserver de Airflow
airflow webserver
airflow scheduler 

