'''Routes for time registration'''
from datetime import datetime, date
from flask import Blueprint, render_template, request
from app.utils import date_utils

bp = Blueprint('time_blueprint', __name__, url_prefix='/time')

@bp.route("/enter", methods=["GET", "POST"])
def enter_time():
    '''Endpoint for time registration'''
    year, weeknumber, daynumber = datetime.isocalendar(datetime.now())
    today = date.today().isoformat()
    today = datetime.today().strftime('%A - %d %B %Y')
    date_info = { 'year': year, 'weeknumber': weeknumber, 'daynumber': daynumber, 'today': today}
    dotime_date_help = date_utils.DoTimeDataHelp()
    days = dotime_date_help.all_days('en')
    return render_template('entertime.html', date_info=date_info, days=days)

@bp.route("/register", methods=["GET","POST"])
def register_time():
    '''Endpoint for receiving time registration records'''
    if request.method == 'POST':
        activity = request.form['activity']
        time_start = request.form['time_start']
        time_end = request.form['time_end']
        return_string =  "Time registration registered"
    else:
        return_string = "GET not allowed"
    return return_string
