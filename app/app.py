'''Initialize application factory'''
from os import environ
from app import create_app
app = create_app()

if __name__ == "__main__":
    app.logger.info('APP Started')
    app.run()
    