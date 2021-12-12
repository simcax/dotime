#!/bin/bash
export DB_PASSWORD=
export DB_USERNAME=root
export DB_NAME=dotimetest
export DB_HOST=localhost
export DB_SSL_MODE=disable
export DB_SSL=false
export DB_ROOT_CERT_PATH=$HOME/.postgresql/root.crt
cd database
flyway info
flyway migrate
flyway info