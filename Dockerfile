FROM cgr.dev/chainguard/python:latest-dev AS dev

LABEL maintainer="carsten@skov.codes"

WORKDIR /flask-app

RUN python -m venv venv
ENV PATH="/flask-app/venv/bin:$PATH"
COPY requirements.txt requirements.txt
RUN pip install psycopg2-binary gunicorn
RUN pip install -r requirements.txt

FROM cgr.dev/chainguard/python:latest

WORKDIR /flask-app

COPY ./dotime/ dotime/
COPY ./docker/config config

COPY --from=dev /flask-app/venv /flask-app/venv
ENV FLASK_APP=app
ENV VIRTUAL_ENV=/flask-app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
EXPOSE 30000

ENTRYPOINT ["python", "-m", "gunicorn", "-c", "python:config.gunicorn", "dotime.app:app" ]