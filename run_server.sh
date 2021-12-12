#!/bin/bash
pushd $HOME/projekter/dotime/docker/cockroachdb
if [ `docker-compose top|grep roach|wc -l` -eq 6 ]; then
    echo "Cockroachdb is already running"
else
    echo "Starting Cockroach DB"
    docker-compose up -d
fi
pushd -0
pwd
# Export environment variables
export DB_PASSWORD=
export DB_USERNAME=root
export DB_NAME=dotimetest
export DB_HOST=localhost
export DB_SSL_MODE=required
export DB_SSL=true
export DB_ROOT_CERT_PATH=/tmp/.postgresql/root.crt
export SECRET_KEY=d2563cb665a7b04fac77ccf4
export FLASK_APP=app
flask run --host 0.0.0.0 --port 25000
