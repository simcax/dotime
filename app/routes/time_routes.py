'''Routes for time registration'''
from datetime import datetime, date
import json
from unittest import result
from flask import Blueprint, jsonify, render_template, request, session, jsonify
from app import timereg
from app.utils import date_utils
from app.timereg import register
from app.auth.authentication import login_required

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
        activity = request.form.get('timecode')
        time_start = request.form.get('time_start')
        time_end = request.form.get('time_end')
        if session.get('user_id'):
            user_id = session.get('user_id')
        else:
            user_id = request.form.get('user_id')
        time_reg = register.TimeRegistration(user_id)
        activity_uuid = time_reg.add_activity(activity)
        if time_reg.add_timeregistration(activity_uuid,time_start, time_end):
            return_string =  "Time registration registered"
        else:
            return_string = "Time registration failed"
    else:
        return_string = "GET not allowed"
    return return_string

@bp.route("/activities")
#@login_required
def activities():
    '''Endpoint for getting activities for a user'''
    if session.get('user_id'):
        do_register = register.TimeRegistration(session['user_id'])
        #do_register.add_activity("test2")
        data = do_register.get_activites()
        item_list = do_register.create_select2_data_structure_for_ajax_call(data)
        return jsonify(item_list)
    return "No User"
