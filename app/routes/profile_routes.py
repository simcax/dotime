'''Routes for profile creation'''

from flask import Blueprint, render_template, request,session, flash, g
from app.profile.profile import ProfileHandling
from app.auth.authentication import login_required
bp = Blueprint('profile_blueprint', __name__, url_prefix='/profile')

@bp.route("/create", methods=["GET", "POST"])
def create_profile():
    '''Endpoint for creating a profile'''
    if request.method == 'POST':
        username = request.form['profileUsername']
        email = request.form['profileEmail']
        password = request.form['profilePassword']
        prof = ProfileHandling()
        user = prof.add_user(username,password,email)
        if user:
            return_value = render_template('profile_created.html', user = user)
        else:
            return_value = render_template("profile_creation_failed.html")
    else:
        return_value = render_template('create_profile.html')
    return return_value

@bp.route("/info")
def profile_info():
    '''Endpoint to inform about user info'''
    return "This is the profile info endpoint"

@bp.route("/me")
@login_required
def profile():
    '''Endpoint to show information about your own profile'''
    prof = ProfileHandling()
    users_id = session['user_id']
    userdata = prof.get_user_data(users_id)
    return render_template("profile_me.html", userdata=userdata)

@bp.route("/update", methods=["POST"])
def update_profile():
    '''Endpoint for updating a profile'''
    # Mock userdata for now
    prof = ProfileHandling()
    users_id = session['user_id']
    userdata = prof.get_user_data(users_id)
    #userdata = {'email': "", 'username': ""}
    new_email = request.form['profileEmail']
    if prof.update_profile(users_id,new_email):
        flash("Profile updated")
    else:
        flash("Profile update failed")
    return render_template("profile_me.html", userdata = userdata)

@bp.route("/changePassword", methods=['GET','POST'])
@login_required
def change_password():
    '''Endpoint for the change password form'''
    if request.method == 'GET':
        return_is = render_template("change_password.html")
    else:
        if request.form['new_password_1'] == request.form['new_password_2']:
            new_password = request.form['new_password_1']
            users_id = session['user_id']
            prof = ProfileHandling()
            email = prof.get_email_by_uuid(users_id)
            if prof.update_password(users_id,email,request.form['current_password'],new_password):
                flash("Password changed")
                return_is = render_template("change_password.html")
        else:
            flash("Passwords don't match")
            return_is = render_template("change_password.html")
    return return_is