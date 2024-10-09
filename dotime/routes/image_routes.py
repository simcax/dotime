"""Routes to serve static images"""

from flask import send_from_directory, Blueprint

bp1 = Blueprint("images_blueprint", __name__, url_prefix="/images")


@bp1.route("/hello.jpg")
def hello_jpg():
    """Serve hello.jpg"""
    return send_from_directory("static/images", "hello.jpg", mimetype="image/jpg")


@bp1.route("/oops.jpg")
def oops_jpg():
    """Serve oops.jph"""
    return send_from_directory("static/images", "oops.jpg", mimetype="image/jpg")


@bp1.route("/welcome.jpg")
def welcome_jpg():
    """Serve welcome.jpg"""
    return send_from_directory("static/images", "welcome.jpg", mimetype="image/jpg")


@bp1.route("/frontpage_welcome.jpg")
def frontpage_welcome_jpg():
    """Serve frontpage_welcome.jpg"""
    return send_from_directory(
        "static/images", "annie-spratt-QckxruozjRg-unsplash.jpg", mimetype="image/jpg"
    )


@bp1.route("/dotime_logo.png")
def dotime_logo_png():
    """Serve dotime_logo.png"""
    return send_from_directory("static/images", "dotime_logo.png", mimetype="image/jpg")


@bp1.route("/dotime_logo_only.png")
def dotime_logo_only_png():
    """Serve dotime_logo_only.png"""
    return send_from_directory(
        "static/images", "dotime_logo_only.png", mimetype="image/jpg"
    )


@bp1.route("/datepicker_feature.png")
def datepicker_feature_png():
    """Serve datepicker_feature.png"""
    return send_from_directory(
        "static/images", "datepicker_feature.png", mimetype="image/png"
    )
