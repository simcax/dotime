'''Routes for session variables'''

from flask import Blueprint, request, session
import html

bp = Blueprint('session_blueprint', __name__, url_prefix='/session')

@bp.route("/set", methods=["GET", "POST"])
def set_session_value():
    '''Endpoint for setting a session value'''
    if request.args.get('value'):
        value = request.args.get('value')
        session['test-value'] = value
        return_str = f"Session value set to: {value}"
    else:
        return_str = "No session value set"
    return html.escape(return_str)

@bp.route("/getTest")
def get_session_value():
    '''Retrieve test session value'''
    return f"Session var is: {session['test-value']}"
