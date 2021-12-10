'''Do Time Flask App'''
from flask import Flask


def create_app(test_config=None):
    '''App factory'''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config:
        print("Test config is set")

    @app.route("/")
    def home():
        return "Welcome to doTime! It will be awesome :-)"
    return app
