#!/bin/bash
export DB_PASSWORD=
export DB_USERNAME=root
export DB_NAME=dotimetest
export DB_HOST=localhost
export DB_SSL_MODE=disable
export DB_SSL=false
export DB_ROOT_CERT_PATH=$HOME/.postgresql/root.crt
export CDB_CLUSTER=pink-gopher-2382
export DB_CONNECTION_STRING="postgresql://${DB_USERNAME}:${DB_PASSWORD}@${DB_HOST}:26257/defaultdb?sslmode=${DB_SSL_MODE}&sslrootcert=$DB_ROOT_CERT_PATH&options=--cluster%3D$CDB_CLUSTER"
cockroach sql --url $DB_CONNECTION_STRING --execute "SHOW DATABASES"
cockroach sql --url "$DB_CONNECTION_STRING" --execute "DROP DATABASE $DB_NAME;CREATE DATABASE $DB_NAME"
cd database
flyway info
flyway repair
flyway migrate
flyway info