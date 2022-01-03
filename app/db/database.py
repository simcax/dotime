'''Database connectivity'''
from os import environ
import psycopg2
from flask import current_app

class Database:
    '''Class to handle database connectivity'''
    db_host = environ.get('DB_HOST','localhost')
    db_name = environ.get('DB_NAME','dotimetest')
    db_username = environ.get('DB_USERNAME','root')
    db_password = environ.get('DB_PASSWORD','')
    db_ssl = environ.get('DB_SSL','false')
    db_sslmode = environ.get('DB_SSLMODE','disable')
    db_connection_string = ''
    db_ssl_settings = ''

    def __init__(self) -> None:
        '''Initialize the database settings'''
        if self.db_ssl == 'false' and self.db_sslmode == 'disable':
            self.db_ssl_settings = "sslmode=disable"
        else:
            self.db_ssl_settings = "sslmode=verify-full"
        self.db_connection_string = f"postgresql://{self.db_username.strip()}:{self.db_password.strip()}@{self.db_host.strip()}:26257/{self.db_name.strip()}?{self.db_ssl_settings.strip()}"

    def connect(self):
        '''Get a new connection to the database'''
        try:
            current_app.logger.info('Connecting to the database')
            conn = psycopg2.connect(self.db_connection_string)
        except psycopg2.DatabaseError as error:
            current_app.logger.info(f"Couldn't connect: {error}")
            conn = False
        return conn
