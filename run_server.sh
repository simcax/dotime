#!/bin/bash
if [ `docker ps -a -f name=^redis|grep redis|wc -l` -eq 1 ];then 
    echo "Redis container exists"
    docker start redis
else
    echo "Starting redis"
    docker run -d -p 6379:6379 redis --name redis
fi
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
export DB_SSL_MODE=disable
export DB_SSL=false
export DB_ROOT_CERT_PATH=/tmp/.postgresql/root.crt
export SECRET_KEY=d2563cb665a7b04fac77ccf4
export SESSION_REDIS=redis://localhost:6379
export SESSION_TYPE=redis
export REDIS_HOST=localhost
export FLASK_APP=app
export FLASK_ENV=DEVELOPMENT
export FLASK_DEBUG=TRUE
flask run --host 0.0.0.0 --port 25000
