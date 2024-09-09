#!/bin/bash

# Obtener el nombre del Codespace
CODESPACE_NAME=$(echo $CODESPACE_NAME)

# Generar la URL dinámica
WEB_SERVER_HOST="https://${CODESPACE_NAME}-8080.app.github.dev"

# Reemplazar en el archivo .env
echo "WEB_SERVER_HOST=$WEB_SERVER_HOST" >> .env
