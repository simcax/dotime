'''Do Time Flask App'''
from os import environ, urandom
from socket import gethostname
import logging
from flask import Flask, render_template, send_from_directory, session
from flask_session import Session
import redis

def create_app(test_config=None):
    '''App factory'''
    redis_host = environ.get('REDIS_HOST','localhost')
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=environ.get('SECRET_KEY',urandom(12).hex()),
        SESSION_TYPE = 'redis',
        SESSION_REDIS = redis.from_url(f"redis://{redis_host}:6379"),
        SESSION_PERMANENT = True,
        SESSION_USE_SIGNER = True,
        SESSION_COOKIE_SECURE = True,
        SESSION_COOKIE_DOMAIN = environ.get('SESSION_COOKIE_DOMAIN','127.0.0.1'),
        SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME','DoTime')
    )
    if test_config:
        app.logger.info("Test config is set")
    app.logger.info(app.config)
    sess = Session()
    with app.app_context():
        sess.init_app(app)
        from app.routes import (
            profile_routes, health_routes, auth_routes, image_routes, session_routes, time_routes
        )
        app.register_blueprint(image_routes.bp1)
        app.register_blueprint(profile_routes.bp)
        app.register_blueprint(health_routes.bp1)
        app.register_blueprint(auth_routes.bp1)
        app.register_blueprint(session_routes.bp)
        app.register_blueprint(time_routes.bp)
        @app.route("/")
        def home():
            version = environ.get("VERSION")
            hostname = gethostname()
            return render_template('home.html', hostname=hostname, version=version)
        @app.route("/background.css")
        def background_css():
            return send_from_directory('static/css','background.css',mimetype='text/css')
        app.logger.info("App routes loaded")
        return app
