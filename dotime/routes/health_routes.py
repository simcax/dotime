"""Routes for health check of application"""

from flask import Blueprint, render_template
from dotime.health.health import Health

bp1 = Blueprint("health_blueprint", __name__, url_prefix="/health")


@bp1.route("/")
def health():
    """Create the health endpoint"""
    h_obj = Health()
    health_string = h_obj.health_string
    if (
        bool(health_string["dbConnection"])
        and health_string["userCount"] != "Database connection failed"
    ):
        return_value = render_template("health.html", healthString=h_obj.health_string)
    else:
        return_value = {"message": health_string}, 400
    return return_value
