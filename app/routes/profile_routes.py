'''Routes for profile creation'''

from flask import Blueprint, render_template

bp = Blueprint('profile_blueprint', __name__, url_prefix='/profile')

@bp.route("/create")
def create_profile():
    '''Endpoint for creating a profile'''
    return render_template('create_profile.html')
