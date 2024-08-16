#!/bin/bash

# Inicializa la base de datos de Airflow
airflow db migrate

# Crea un usuario administrador si no existe (opcional)
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Arranca el scheduler y el webserver de Airflow
airflow scheduler &
airflow webserver
