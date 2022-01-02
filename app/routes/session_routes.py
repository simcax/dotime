'''Routes for session variables'''

from flask import Blueprint, render_template, request, session

bp = Blueprint('session_blueprint', __name__, url_prefix='/session')

@bp.route("/set", methods=["GET", "POST"])
def set_session_value():
    '''Endpoint for setting a session value'''
    if request.args.get('value'):
        value = request.args.get('value')
        session['test-value'] = value
        return f"Session value set to: {value}"
