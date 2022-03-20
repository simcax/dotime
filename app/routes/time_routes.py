'''Routes for time registration'''
from datetime import datetime, timedelta
from flask import (
    Blueprint, current_app, jsonify, render_template, request, session, flash, url_for, redirect
)
from app.profile.settings import SettingsHandling
from app.utils import date_utils
from app.timereg import register, events
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
    
    # Get current commute status
    event_obj = events.HandleEvents()
    commute_status = event_obj.get_commute_status(session.get('user_id'),time_date)
    time_registered = reg.get_registration_time_on_day(time_date)
    settings_obj = SettingsHandling()
    weekday_lengths = settings_obj.get_workweek_day_lengths(session.get('user_id'))
    current_app.logger.info(weekday_lengths)
    weekday_length_hour = weekday_lengths.get(f'workdayLength{daynumber}Hour')
    if weekday_length_hour:
        weekday_length_hour = f"{int(weekday_length_hour):02d}"
    
    weekday_length_minutes = weekday_lengths.get(f'workdayLength{daynumber}Minutes')
    total_time_worked_this_week = reg.get_registration_time_for_week(time_date)
    total_norm_hours_week = settings_obj.get_number_of_work_hours_for_a_week(session.get('user_id'))
    current_app.logger.debug("worked week %s",total_time_worked_this_week)
    percentage_hours_worked_this_week = reg.percentage_worked(session.get('user_id'),time_date)
    current_app.logger.debug("Percentage: %s",percentage_hours_worked_this_week)
    return render_template(
        'entertime.html', date_info=date_info, days=days,
        time_registrations=time_registrations, commute_status=commute_status,
        time_registered=time_registered, weekday_length=f"{weekday_length_hour}:{weekday_length_minutes}",
        time_worked_week=total_time_worked_this_week,
        percentage_hours_worked_this_week=percentage_hours_worked_this_week,
        total_norm_hours_week=total_norm_hours_week
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
            error_message =  "Time registration registered"
        else:
            error_message = "Time registration failed"
        flash(error_message)
        returning = redirect(url_for("time_blueprint.enter_time",showDate=time_date))
    else:
        returning = redirect(url_for("home"))
    return returning

@bp.route("/register/commuteornot", methods=["POST"])
def register_commute_or_not():
    '''Endpoint for registering commuteornot event'''
    request_data = request.get_json()
    toggle_value = request_data['data']
    the_date = request_data['the_date']
    current_app.logger.debug(request_data['data'])
    current_app.logger.debug(request_data['the_date'])
    user_id = session.get('user_id')
    event_obj = events.HandleEvents()
    commute_event_type_uuid = event_obj.get_event_type('CommuteToWork')
    work_from_home_event_type_uuid = event_obj.get_event_type('WorkFromHome')

    if toggle_value == 'commuted':
        on_event_type_uuid = commute_event_type_uuid
        off_event_type_uuid = work_from_home_event_type_uuid
    elif toggle_value == 'workedathome':
        current_app.logger.debug("Setting ON event type workfromhome")
        on_event_type_uuid = work_from_home_event_type_uuid
        off_event_type_uuid = commute_event_type_uuid


    commute_status = event_obj.get_commute_status(user_id,the_date)
    current_app.logger.debug("START commute_status: %s", commute_status)
    turned_off = ""
    turned_on = ""
    if commute_status is None:
        # Turn on the event
        turned_on = event_obj.toggle_event(on_event_type_uuid,the_date,user_id)
        turned_off = 'off'
    elif toggle_value == "workedathome":
        if commute_status == 'WorkFromHome':
            current_app.logger.debug("Already work from home")
            turned_on = 'on'
            turned_off = 'off'
        else:
            current_app.logger.debug("Toggling WorkFromHome on")
            turned_on = event_obj.toggle_event(on_event_type_uuid,the_date,user_id)
            current_app.logger.debug("Toggling commute to work off")
            turned_off = event_obj.toggle_event(off_event_type_uuid,the_date,user_id)
    elif toggle_value == "commuted":
        if commute_status == "CommutedToWork":
            current_app.logger.debug("Commute already set")
            turned_on = 'on'
            turned_off = 'off'
        else:
            current_app.logger.debug("Toggling Commute on")
            turned_on = event_obj.toggle_event(on_event_type_uuid,the_date,user_id)
            turned_off = event_obj.toggle_event(off_event_type_uuid,the_date,user_id)
    elif toggle_value == "didntwork":
        current_app.logger.debug("Toggle value is %s",toggle_value)
        if commute_status == 'WorkFromHome':
            current_app.logger.debug("Setting off value to work from home event type")
            off_event_type_uuid = work_from_home_event_type_uuid
        elif commute_status == 'CommutedToWork':
            current_app.logger.debug("Setting off value to commute to work event type")
            off_event_type_uuid = commute_event_type_uuid
        turned_on = 'on'
        turned_off = event_obj.toggle_event(off_event_type_uuid,the_date,user_id)


    commute_status = event_obj.get_commute_status(user_id,the_date)
    current_app.logger.debug("RESULTING commute_status: %s", commute_status)
    if turned_on == 'on' and turned_off == 'off':
        return_is = "OK"
    else:
        return_is = "error"
    current_app.logger.debug("Date %s, ON; %s, OFF: %s, Returning: %s",
        the_date, turned_on, turned_off,return_is)
    return return_is

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
