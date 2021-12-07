FROM python:3.10.0
RUN apt update
RUN apt install -y gunicorn3
# Upgrade pip 
RUN python3 -m pip install --upgrade pip
RUN python -m venv /venv
COPY ./requirements.txt /
RUN . venv/bin/activate && python -m pip install psycopg2 && python -m pip install -r requirements.txt
COPY ./app /app
ENV FLASK_APP=app
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY ./docker/config /config
COPY ./docker/docker_entrypoint.sh /
RUN chmod +x /docker_entrypoint.sh
WORKDIR /
EXPOSE 30000

ENTRYPOINT [ "./docker_entrypoint.sh" ]
CMD [ "/venv/bin/gunicorn", "-c", "python:config.gunicorn", "app:create_app" ]