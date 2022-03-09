'''Routes for auth/login to the application'''
from flask import (
    Blueprint, render_template, request, flash, session, g, current_app, redirect, url_for
)
from app.profile.profile import ProfileHandling

from app.auth.authentication import Authentication, login_required


bp1 = Blueprint('auth_blueprint', __name__, url_prefix='/auth')

@bp1.route("/login", methods=["GET", "POST"])
def login():
    '''Login endpoint - shows the login page or checks credentials'''
    if request.method == 'POST':
        # Log in user
        email = request.form.get('email')
        password = request.form.get('password')
        next_url = request.form.get('next')
        prof = ProfileHandling()
        user_id = prof.check_credentials(email,password)
        if user_id:
            session['user_id'] = user_id
            current_app.logger.info("User is authenticated")
            if next_url:
                current_app.logger.info("Next url was set to %s",next_url)
                return_is = redirect(next_url)
            else:
                # The user logged in on the home page, and should be redirected
                # to the time registration page - as for now that's where the
                # music is
                flash("You are logged in.")
                return_is = redirect(url_for('time_blueprint.enter_time'))
        else:
            flash("Error logging you in.")
            current_app.logger.info("User was not logged in: %s", email)
            return_is = render_template('loginonly.html',color_class='danger')
    else:
        return_is = render_template('loginonly.html')

    return return_is

@bp1.route("/logout")
def logout():
    '''Log out user'''
    session.clear()
    flash("Logged out")
    return redirect(url_for('home'))

@bp1.route("/unauthorized")
@login_required
def unauthorized():
    '''Endpoint to test for redirection to login due to unatuhorized access'''

@bp1.before_app_request
def load_logged_in_user():
    '''Method checking if the user has a session'''
    user_id = session.get('user_id')
    current_app.logger.debug("load_logged_in_user user_id is currently: %s", user_id)
    if user_id is None:
        g.user = None
    else:
        auth = Authentication()
        user = auth.get_user_data(user_id)
        g.user = user
