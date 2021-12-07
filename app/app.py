from flask import Flask


def create_app(test_confige=None):
    '''App factory'''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    @app.route("/")
    def home():
        return "Welcome to doTime"

    return app