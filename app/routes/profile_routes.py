'''Routes for profile creation'''

from flask import Blueprint, render_template, request

bp = Blueprint('profile_blueprint', __name__, url_prefix='/profile')

@bp.route("/create", methods=["GET", "POST"])
def create_profile():
    '''Endpoint for creating a profile'''
    if request.method == 'POST':
        return "Your profile was created!"
    else:
        return render_template('create_profile.html')
