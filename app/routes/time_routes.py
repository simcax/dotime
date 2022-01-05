'''Routes for time registration'''
from datetime import datetime
from flask import Blueprint, render_template

bp = Blueprint('time_blueprint', __name__, url_prefix='/time')

@bp.route("/enter", methods=["GET", "POST"])
def register_time():
    '''Endpoint for time registration'''
    year, weeknumber, daynumber = datetime.isocalendar(datetime.now())
    date_info = { 'year': year, 'weeknumber': weeknumber, 'daynumber': daynumber}
    return render_template('entertime.html', date_info=date_info)
