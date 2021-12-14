'''Database connectivity'''
from os import environ

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
        self.db_connection_string = f"postgresql://{self.db_username.rstrip()}:\
        {self.db_password.rstrip()}@{self.db_host.rstrip()}:26257/\
        {self.db_name.rstrip()}?{self.db_ssl_settings.rstrip()}"