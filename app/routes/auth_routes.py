'''Routes for auth/login to the application'''
from flask import Blueprint, render_template, request
from app.health.health import Health
from app.profile.profile import ProfileHandling
bp1 = Blueprint('auth_blueprint', __name__, url_prefix='/auth')

@bp1.route("/login", methods=["GET", "POST"]) 
def login():
    '''Login endpoint - shows the login page or checks credentials'''
    if request.method == 'POST':
        # Log in user
        email = request.form['email']
        password = request.form['password']
        prof = ProfileHandling()
        authenticated = prof.check_credentials(email,password)
        if authenticated:
            return_is = render_template('loggedin.html')
        else:
            return_is = render_template('loginonly.html',login_error="Error logging you in.")
    else:
        return_is = render_template('loginonly.html')
    
    return return_is
