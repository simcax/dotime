'''Do Time Flask App'''
from flask import Flask, render_template


def create_app(test_config=None):
    '''App factory'''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config:
        print("Test config is set")

    with app.app_context():
        from app.routes import profile_routes
        app.register_blueprint(profile_routes.bp)
        @app.route("/")
        def home():
            return render_template('home.html')
        return app
