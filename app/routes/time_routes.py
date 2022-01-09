'''Routes for time registration'''
from datetime import datetime
from flask import Blueprint, render_template
from app.utils import date_utils

bp = Blueprint('time_blueprint', __name__, url_prefix='/time')

@bp.route("/enter", methods=["GET", "POST"])
def enter_time():
    '''Endpoint for time registration'''
    year, weeknumber, daynumber = datetime.isocalendar(datetime.now())
    date_info = { 'year': year, 'weeknumber': weeknumber, 'daynumber': daynumber}
    dotime_date_help = date_utils.DoTimeDataHelp()
    days = dotime_date_help.all_days('en')
    return render_template('entertime.html', date_info=date_info, days=days)
