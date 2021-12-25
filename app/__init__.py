'''Do Time Flask App'''
from os import environ, urandom
from flask import Flask, render_template, send_from_directory

def create_app(test_config=None):
    '''App factory'''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=environ.get('SECRET_KEY',urandom(12).hex())
    )

    if test_config:
        print("Test config is set")

    with app.app_context():
        from app.routes import profile_routes, health_routes, auth_routes
        app.register_blueprint(profile_routes.bp)
        app.register_blueprint(health_routes.bp1)
        app.register_blueprint(auth_routes.bp1)
        @app.route("/")
        def home():
            return render_template('home.html')
        @app.route("/background.css")
        def background_css():
            return send_from_directory('static/css','background.css',mimetype='text/css')
        return app
