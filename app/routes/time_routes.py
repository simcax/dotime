'''Routes for time registration'''
from datetime import date, datetime
from flask import Blueprint, request, session, render_template

bp = Blueprint('time_blueprint', __name__, url_prefix='/time')

@bp.route("/enter", methods=["GET", "POST"])
def register_time():
    year, weeknumber, daynumber = datetime.isocalendar(datetime.now())
    return render_template('entertime.html', weeknumber=weeknumber)
