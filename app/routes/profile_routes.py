'''Routes for profile creation'''

from flask import Blueprint, render_template, request,session
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
