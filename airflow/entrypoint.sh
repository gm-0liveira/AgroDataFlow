#!/bin/bash
# entrypoint.sh

set -e

echo ">> Aguardando o banco de dados ficar disponível (Postgres)..."

while ! nc -z postgres 5432; do
  sleep 2
done

echo ">> Banco de dados disponível!"

# Inicializa o banco de dados somente se for a primeira vez
airflow db upgrade

# Cria o usuário admin se ainda não existir
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com || true

# Executa o comando (webserver ou scheduler)
exec airflow "$@"
