"""Routes for everything, which does not belong anywere else"""

from flask import send_from_directory, Blueprint

bp = Blueprint("general_blueprint", __name__)


@bp.route("/favicon.ico")
def favicon():
    """Serve favicon.ico"""
    return send_from_directory("static/images", "favicon.ico", mimetype="image/jpg")
