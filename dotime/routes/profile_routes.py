"""Routes for profile creation"""

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    flash,
    current_app,
    url_for,
)
from dotime.profile.profile import ProfileHandling
from dotime.profile.settings import SettingsHandling
from dotime.auth.authentication import login_required

bp = Blueprint("profile_blueprint", __name__, url_prefix="/profile")


@bp.route("/create", methods=["GET", "POST"])
def create_profile():
    """Endpoint for creating a profile"""
    if request.method == "POST":
        username = request.form["profileUsername"]
        email = request.form["profileEmail"]
        password = request.form["profilePassword"]
        prof = ProfileHandling()
        user = prof.add_user(username, password, email)
        # User created, so let's add default settings
        settings_obj = SettingsHandling()
        if user:
            settings_obj.add_defaults(user.get("users_id"))
            # return_value = render_template('profile_created.html', user = user)
            flash("Your profile was created. Please login")
            return_value = redirect(url_for("auth_blueprint.login"))
        else:
            return_value = render_template("profile_creation_failed.html")
    else:
        return_value = render_template("create_profile.html")
    return return_value


@bp.route("/info")
def profile_info():
    """Endpoint to inform about user info"""
    return "This is the profile info endpoint"


@bp.route("/me")
@login_required
def profile():
    """Endpoint to show information about your own profile"""
    prof = ProfileHandling()
    users_id = session["user_id"]
    userdata = prof.get_user_data(users_id)
    return render_template("profile_me.html", userdata=userdata)


@bp.route("/update", methods=["POST"])
def update_profile():
    """Endpoint for updating a profile"""
    # Mock userdata for now
    prof = ProfileHandling()
    users_id = session["user_id"]
    userdata = prof.get_user_data(users_id)
    # userdata = {'email': "", 'username': ""}
    new_email = request.form["profileEmail"]
    if prof.update_profile(users_id, new_email):
        flash("Profile updated")
    else:
        flash("Profile update failed")
    return render_template("profile_me.html", userdata=userdata)


@bp.route("/changePassword", methods=["GET", "POST"])
@login_required
def change_password():
    """Endpoint for the change password form"""
    if request.method == "GET":
        return_is = render_template("change_password.html")
    else:
        if request.form["new_password_1"] == request.form["new_password_2"]:
            new_password = request.form["new_password_1"]
            users_id = session["user_id"]
            prof = ProfileHandling()
            email = prof.get_email_by_uuid(users_id)
            if prof.update_password(
                users_id, email, request.form["current_password"], new_password
            ):
                flash("Password changed")
                return_is = render_template("change_password.html")
        else:
            flash("Passwords don't match")
            return_is = render_template("change_password.html")
    return return_is


@bp.route("/settings", methods=["GET", "POST"])
@login_required
def profile_settings():
    """Endpoint for a user to edit settings"""
    settings_obj = SettingsHandling()
    settings = settings_obj.get_settings(session["user_id"])
    if request.method == "POST":
        for i in range(1, 8):
            current_key = f"workdayLength{i}Hour"
            current_value = request.form[current_key]
            updated = check_and_update(
                settings_obj, settings, current_key, current_value
            )
            if updated:
                current_app.logger.debug(f"{current_key} updated to {current_value}")
            current_key = f"workdayLength{i}Minutes"
            current_value = request.form[current_key]
            updated = check_and_update(
                settings_obj, settings, current_key, current_value
            )
            if updated:
                current_app.logger.debug(f"{current_key} updated to {current_value}")
    else:
        if len(settings) == 0:
            settings_obj.add_defaults(session["user_id"])
        settings = settings_obj.get_settings(session["user_id"])
    workweek_day_lengths = settings_obj.get_workweek_day_lengths(session["user_id"])
    return render_template(
        "profile_settings.html", settings=settings, workday_lengths=workweek_day_lengths
    )


def check_and_update(settings_obj, settings, current_key, current_value):
    """Checks if the value was updated and needs to be comitted to the database"""
    updated = False
    if current_value != settings.get(current_key):
        updated = settings_obj.add_setting(
            session["user_id"], current_key, current_value
        )
    elif current_value == 0:
        # Handle if the value is zero
        updated = settings_obj.add_setting(
            session["user_id"], current_key, current_value
        )
    return updated
