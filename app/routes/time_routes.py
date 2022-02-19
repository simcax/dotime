'''Routes for time registration'''
from datetime import datetime, timedelta
from flask import (
    Blueprint, current_app, jsonify, render_template, request, session, flash, url_for, redirect
)
from app.utils import date_utils
from app.timereg import register
from app.auth.authentication import login_required

bp = Blueprint('time_blueprint', __name__, url_prefix='/time')

@bp.route("/enter", methods=["GET", "POST"])
def enter_time():
    '''Endpoint for time registration'''
    year, weeknumber, daynumber = datetime.isocalendar(datetime.now())
    if request.args.get('showDate') is None:
        today = datetime.now()
    else:
        today = datetime.strptime(request.args.get('showDate'),'%Y-%m-%d')
        current_app.logger.debug("Setting today to: %s", today)
    yesterday = today + timedelta(days=-1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    tomorrow = today + timedelta(days=1)
    tomorrow = tomorrow.strftime('%Y-%m-%d')
    today_text = today.strftime('%A - %d %B %Y')
    time_date = today.strftime("%Y-%m-%d")
    date_info = {
        'year': year, 'weeknumber': weeknumber, 'daynumber': daynumber, 'today': today_text,
        'time_date': time_date, 'tomorrow': tomorrow, 'yesterday': yesterday}
    dotime_date_help = date_utils.DoTimeDataHelp()
    days = dotime_date_help.all_days('en')
    reg = register.TimeRegistration(session.get('user_id'))
    time_registrations = reg.get_registrations(time_date)
    current_app.logger.debug(time_registrations)
    return render_template(
        'entertime.html', date_info=date_info, days=days,
        time_registrations=time_registrations
        )

@bp.route("/register", methods=["GET","POST"])
@login_required
def register_time():
    '''Endpoint for receiving time registration records'''
    if request.method == 'POST':
        activity = request.form.get('timecode')
        time_start = request.form.get('time_start')
        time_end = request.form.get('time_end')
        time_date = request.form.get('time_date')
        if session.get('user_id'):
            user_id = session.get('user_id')
        else:
            user_id = request.form.get('user_id')
        time_reg = register.TimeRegistration(user_id)
        # Due to the way select2 works, an activity uuid will be sent, when a 
        # pre-existing activity is selected and registered. In that case, it
        # shouldn't be added - it is already in the database.
        # So a check is performed to see if it is a uuid already existing.
        # This might be done smarter at some point...
        if not time_reg.is_activityuuid(activity):
            activity_uuid = time_reg.add_activity(activity)
        else:
            # The method was given an activity UUID
            activity_uuid = activity
        if time_reg.add_timeregistration(activity_uuid, time_date,time_start, time_end):
            return_string =  "Time registration registered"
        else:
            return_string = "Time registration failed"
        flash(return_string)
        return redirect(url_for("time_blueprint.enter_time",showDate=time_date))

@bp.route("/activities")
#@login_required
def activities():
    '''Endpoint for getting activities for a user'''
    if session.get('user_id'):
        do_register = register.TimeRegistration(session['user_id'])
        data = do_register.get_activites()
        item_list = do_register.create_select2_data_structure_for_ajax_call(data)
        return jsonify(item_list)
    return "No User"

@bp.route("/activity/name/<activity_name>")
def get_activity_by_name(activity_name):
    '''Endpoint for getting a specific activity'''
    do_register = register.TimeRegistration(session['user_id'])
    data = do_register.get_activites(activity_name=activity_name)
    item_list = do_register.create_select2_data_structure_for_ajax_call(data,no_list='true')
    return jsonify(item_list)

@bp.route("/activity/uuid/<activity_uuid>")
def get_activity_by_uuid(activity_uuid):
    '''Endpoint for getting a specific activity'''
    do_register = register.TimeRegistration(session['user_id'])
    data = do_register.get_activites(activity_uuid=activity_uuid)
    item_list = do_register.create_select2_data_structure_for_ajax_call(data,no_list='true')
    return jsonify(item_list)
