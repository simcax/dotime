'''Test time registration methods'''
import datetime
from datetime import date, time
from random import randint, choice
from venv import create
import uuid
import pytest
from app.timereg.register import TimeRegistration
from app.profile.profile import ProfileHandling
from app.timereg.events import HandleEvents
from app.utils.date_utils import DoTimeDataHelp
from test_utils import TestUtils
from conftest import login, logout

def add_activity_registrations(user_id,number_of_activities,number_of_registrations, date_of_registrations=None):
    '''
        Creates <number_of_activities> and afterwards registers 
        <number_of_registrations> registrations
    '''
    time_reg = TimeRegistration(user_id)
    tu = TestUtils()
    activities = []
    for i in range(0,number_of_activities):
        activity_name_str = tu.createRandomString()
        activity_uuid = time_reg.add_activity(activity_name_str)
        activities.append(activity_uuid)
    start_timefrom = datetime.datetime.now()
    if date_of_registrations == None:
        thisdate = start_timefrom.strftime('%Y-%m-%d')
    else:
        thisdate = date_of_registrations
    for i in range(0, number_of_registrations):
        if i == 0:
            timefrom = start_timefrom
        else:
            timefrom = timeto_timestamp + datetime.timedelta(minutes=1)
        timeto_timestamp = timefrom + datetime.timedelta(minutes=2)
        timefrom = timefrom.strftime('%I:%M')
        timeto = timeto_timestamp.strftime('%I:%M')
        this_activity_uuid = choice(activities)
        timereg_added = time_reg.add_timeregistration(this_activity_uuid, thisdate, timefrom, timeto)

        

def test_add_activity(create_user):
    '''Test an activity can be added to the activity table'''
    userdata = create_user['info']
    user_id = userdata['users_id']
    time_reg = TimeRegistration(user_id)
    tu = TestUtils()
    activity_name_str = tu.createRandomString()
    activity_uuid = time_reg.add_activity(activity_name_str)
    assert isinstance(activity_uuid, str)

def test_add_timereg_row(create_user):
    '''Test adding a time registration row'''
    userdata = create_user['info']
    user_id = userdata['users_id']
    time_reg = TimeRegistration(user_id)
    tu = TestUtils()
    activity_name_str = tu.createRandomString()
    activity_uuid = time_reg.add_activity(activity_name_str)
    timefrom = datetime.datetime.now()
    timeto = timefrom + datetime.timedelta(minutes=2)
    thisdate = timefrom.strftime('%Y-%m-%d')
    timefrom = timefrom.strftime('%I:%M')
    timeto = timeto.strftime('%I:%M')
    assert isinstance(activity_uuid, str)
    timereg_added = time_reg.add_timeregistration(activity_uuid, thisdate, timefrom, timeto)
    assert timereg_added == True

def test_add_timereg_wrong_order(create_user,app_test_context):
    '''Test getting an error when adding a time reg record with to before from timestamp'''
    with app_test_context:
        userdata = create_user['info']
        user_id = userdata['users_id']
        time_reg = TimeRegistration(user_id)
        tu = TestUtils()
        activity_name_str = tu.createRandomString()
        activity_uuid = time_reg.add_activity(activity_name_str)
        timeto = datetime.datetime.now()
        timefrom = timeto + datetime.timedelta(minutes=2)
        thisdate = timefrom.strftime('%Y-%m-%d')
        timefrom = timefrom.strftime('%I:%M')
        timeto = timeto.strftime('%I:%M')
        
        assert isinstance(activity_uuid, str)
        timereg_added = time_reg.add_timeregistration(activity_uuid, thisdate, timefrom, timeto,testing=True)
        assert timereg_added == False

# TODO: Need to find a solution for this.
# def test_add_timereg_correct_timestamps(create_user):
#     '''Test a timestamp check is carried out when submitting a timereg entry'''
#     userdata = create_user['info']
#     user_id = userdata['users_id']
#     time_reg = TimeRegistration(user_id)
#     tu = TestUtils()
#     activity_name_str = tu.createRandomString()
#     activity_uuid = time_reg.add_activity(activity_name_str)
#     timefrom = datetime.datetime.now()
#     timeto = str(timefrom + datetime.timedelta(minutes=2)) + "1a"
#     assert isinstance(activity_uuid, str)
#     timereg_added = time_reg.add_timeregistration(activity_uuid, timefrom, timeto)
#     assert timereg_added == False

def test_add_timereg_overlapping_registrations(create_user,app_test_context):
    '''Tests an error will occour if a timeregistration overlaps another timeregistration'''
    with app_test_context:
        userdata = create_user['info']
        user_id = userdata['users_id']
        time_reg = TimeRegistration(user_id)
        tu = TestUtils()
        activity_name_str = tu.createRandomString()
        activity_uuid = time_reg.add_activity(activity_name_str)

        timefrom1 = datetime.datetime.now()
        timeto1 = timefrom1 + datetime.timedelta(minutes=2)
        timefrom2 = timefrom1 + datetime.timedelta(minutes=1)
        timeto2 = timefrom2 + datetime.timedelta(minutes=10)
        thisdate = timefrom1.strftime('%Y-%m-%d')
        timefrom1 = timefrom1.strftime('%I:%M')
        timeto1 = timeto1.strftime('%I:%M')
        
        
        timefrom2 = timefrom2.strftime('%I:%M')
        timeto2 = timeto2.strftime('%I:%M')
        assert isinstance(activity_uuid, str)
        timereg_added_1 = time_reg.add_timeregistration(activity_uuid, thisdate, timefrom1, timeto1,testing=True)
        timereg_added_2 = time_reg.add_timeregistration(activity_uuid, thisdate, timefrom2, timeto2,testing=True)
        assert timereg_added_1 == True
        # Since the second timereg row overlaps with the first, insertion should fail.
        assert timereg_added_2 == False

def test_get_activities(create_user,app_test_context):
    with app_test_context:
        userdata = create_user['info']
        user_id = userdata['users_id']
        tu = TestUtils()
        time_reg = TimeRegistration(user_id)
        activity_name_str = tu.createRandomString()
        activity_uuid = time_reg.add_activity(activity_name_str)
        activity_name_str = tu.createRandomString()
        activity_uuid = time_reg.add_activity(activity_name_str)
        activites = time_reg.get_activites()
        assert len(activites) == 2

def test_get_activity(create_user,app_test_context):
    '''Test getting a specific activity by uuid'''
    with app_test_context:
        userdata = create_user['info']
        user_id = userdata['users_id']
        tu = TestUtils()
        time_reg = TimeRegistration(user_id)
        activity_name_str = tu.createRandomString()
        activity_uuid1 = time_reg.add_activity(activity_name_str)
        activity_name_str = tu.createRandomString()
        activity_uuid2 = time_reg.add_activity(activity_name_str)
        activites = time_reg.get_activites(activity_uuid=activity_uuid1)
        assert len(activites) == 1

def test_get_timecodes_endpoint(client, create_user):
    login(client,create_user['email'], create_user['password'])
    rv = client.get("/time/activities")
    assert rv.status_code == 200

def test_get_registered_time_on_today(create_user,app_test_context):
    with app_test_context:
        userdata = create_user['info']
        user_id = userdata['users_id']
        add_activity_registrations(user_id,2,4)
        time_reg = TimeRegistration(user_id)
        registration_date = datetime.datetime.now().strftime('%Y-%m-%d')
        registrations = time_reg.get_registrations(registration_date)
        assert len(registrations) == 4

def test_add_activity_on_yesterday(create_user,app_test_context):
    with app_test_context:
        userdata = create_user['info']
        user_id = userdata['users_id']
        date_of_registrations = datetime.datetime.now()
        date_of_registrations = date_of_registrations + datetime.timedelta(days=-1)
        yesterday = date_of_registrations.strftime('%Y-%m-%d')
        add_activity_registrations(user_id,2,4, yesterday)
        # Change date to today, and add some more registrations
        today = date_of_registrations + datetime.timedelta(days=1)
        today = today.strftime('%Y-%m-%d')
        add_activity_registrations(user_id,2,4, today)
        time_reg = TimeRegistration(user_id)
        # Get the registrations from yesterday
        registrations = time_reg.get_registrations(yesterday)
        assert len(registrations) == 4

def test_seeing_if_uuid_exists(create_user, app_test_context):
    userdata = create_user['info']
    user_id = userdata['users_id']
    tu = TestUtils()
    time_reg = TimeRegistration(user_id)
    with app_test_context:
        activity_name_str = tu.createRandomString()
        activity_uuid = time_reg.add_activity(activity_name_str)
        length = len(activity_uuid)
        is_activity_uuid = time_reg.is_activityuuid(activity_uuid)
        assert is_activity_uuid == True

def test_seeing_if_uuid_exists_with_non_existing_uuid(create_user):
    userdata = create_user['info']
    user_id = userdata['users_id']
    tu = TestUtils()
    time_reg = TimeRegistration(user_id)
    test_uuid = uuid.uuid4()
    is_activity_uuid = time_reg.is_activityuuid(test_uuid)
    assert is_activity_uuid == False

def test_seeing_if_uuid_exists_with_string(create_user):
    userdata = create_user['info']
    user_id = userdata['users_id']
    tu = TestUtils()
    time_reg = TimeRegistration(user_id)
    test_uuid = 'test'
    is_uuid = time_reg.is_activityuuid(test_uuid)
    assert is_uuid == False

def test_having_end_time_in_one_registration_be_equal_to_start_time_of_next_registration(create_user,app_test_context):
    '''
        A test to make sure the end time of one registration can overlap with the start time of the
        next registration. I.e. one registration ends on 06:14, and the next should then be able
        to start at 6:14. This makes the most visual sense in the registration form and each minute
        will then be possible to register.
    '''
    userdata = create_user['info']
    user_id = userdata['users_id']
    tu = TestUtils()
    time_reg = TimeRegistration(user_id)
    with app_test_context:
        activity_name_str = tu.createRandomString()
        activity_uuid = time_reg.add_activity(activity_name_str)
        start_timefrom = datetime.datetime.now()
        thisdate = start_timefrom.strftime('%Y-%m-%d')
        # Base timestamps
        timefrom_timestamp = start_timefrom
        timeto_timestamp = timefrom_timestamp + datetime.timedelta(minutes=2)
        # hour and minute times of first entry
        timefrom1 = timefrom_timestamp.strftime('%I:%M')
        timeto1 = timeto_timestamp.strftime('%I:%M')
        # Timestamps for 2nd entry
        timefrom2_timestamp = timeto_timestamp
        timeto2_timestamp = timefrom2_timestamp + datetime.timedelta(minutes=2)
        # Hour and minute times of 2nd entry
        timefrom2 = timefrom2_timestamp.strftime('%I:%M')
        timeto2 = timeto2_timestamp.strftime('%I:%M')
        time_reg.add_timeregistration(activity_uuid,thisdate,timefrom1,timeto1,testing=True)
        timefrom2_full = f"{thisdate} {timefrom2}"
        timestamp_is_not_here = time_reg.timestamp_is_not_registered(timefrom2_full)
        assert timestamp_is_not_here == True


def test_event_type_is_not_registered(create_user):
    '''
        Test it is possible to see an event type is not registered in the events table for a user 
        on a specific date
    '''
    # Get a random event type uuid
    event_type_uuid = get_random_event_type_uuid()
    # Get the user id
    userdata = create_user['info']
    user_id = userdata['users_id']
    # Set a date
    this_date = datetime.datetime.now().strftime('%Y-%m-%d')

    event_obj = HandleEvents()
    # Is the event registered for the user on this date?
    registered = event_obj.is_event_registered(event_type_uuid,this_date,user_id)
    assert registered == False

def test_adding_event_type_for_user_on_date(create_user):
    '''
        Test adding an event on a specific date for a user
    '''
    # Get a random event type uuid
    event_type_uuid = get_random_event_type_uuid()
    # Get the user id
    userdata = create_user['info']
    user_id = userdata['users_id']
    # Set a date
    this_date = datetime.datetime.now().strftime('%Y-%m-%d')

    event_obj = HandleEvents()
    # Is the event registered for the user on this date?
    registered = event_obj.add_event(event_type_uuid,this_date,user_id)
    assert registered == True

def test_deleting_event_type_for_user_on_date(create_user,app_test_context):
    '''
        Test removing an event on a specific date for a user
    '''
    with app_test_context:
        # Get a random event type uuid
        event_type_uuid = get_random_event_type_uuid()
        # Get the user id
        userdata = create_user['info']
        user_id = userdata['users_id']
        # Set a date
        this_date = datetime.datetime.now().strftime('%Y-%m-%d')

        event_obj = HandleEvents()
        # Register the event
        registered = event_obj.add_event(event_type_uuid,this_date,user_id)
        deleted = event_obj.delete_event(event_type_uuid,this_date,user_id)
        assert deleted == True

def test_toggling_event_type_on(create_user):
    '''
        Test toggling an event on a date. If the event type is not registered on a date, and it is 
        toggled, then add it it. 
    '''
    # Get the user id
    userdata = create_user['info']
    user_id = userdata['users_id']
    
    event_obj = HandleEvents()
    # Set the date of the event happening
    this_date = datetime.datetime.now().strftime('%Y-%m-%d')
    # Make sure the default event types are registered
    event_obj.initialize_events()
    # Get a random event type uuid
    event_type_uuid = get_random_event_type_uuid()
    # The event would not have been registered for this user, so we should have it toggled on.
    # The method can return False (= failure), on (= toggled on) or off (= toggled off)
    toggle = event_obj.toggle_event(event_type_uuid,this_date,user_id)
    assert toggle == 'on'

def test_toggling_event_type_off(create_user,app_test_context):
    '''
        Test toggling an event on a date. If the event type is not registered on a date, and it is 
        toggled, then add it it. 
    '''
    with app_test_context:
        # Get the user id
        userdata = create_user['info']
        user_id = userdata['users_id']
        
        event_obj = HandleEvents()
        # Set the date of the event happening
        this_date = datetime.datetime.now().strftime('%Y-%m-%d')
        # Make sure the default event types are registered
        event_obj.initialize_events()
        # Get a random event type uuid
        event_type_uuid = get_random_event_type_uuid()
        # The event would not have been registered for this user, so we should have it toggled on.
        # The method can return False (= failure), on (= toggled on) or off (= toggled off)
        toggle = event_obj.toggle_event(event_type_uuid,this_date,user_id)
        toggle = event_obj.toggle_event(event_type_uuid,this_date,user_id)
        assert toggle == 'off'


def get_random_event_type_uuid():
    event_obj = HandleEvents()
    # Get the even types
    event_types = event_obj._get_event_types()
    # Let's choose an event type at random
    random_element_number = randint(0,len(event_types)-1)
    random_event_type_name = event_types[random_element_number]
    # Retrieve the uuid of the event type
    event_type_uuid = event_obj.get_event_type(random_event_type_name)
    return event_type_uuid

def test_get_event_type_for_date(create_user):
    # Get the user id
    userdata = create_user['info']
    user_id = userdata['users_id']
    
    event_obj = HandleEvents()
    # Set the date of the event happening
    this_date = datetime.datetime.now().strftime('%Y-%m-%d')
    # Make sure the default event types are registered
    event_obj.initialize_events()
    # Get a random event type uuid
    event_type_uuid = get_random_event_type_uuid()
    # Check the event does not exist - since the user is new it is not registered on this date
    registration_status = event_obj.is_event_registered(event_type_uuid,this_date,user_id)
    assert registration_status == False

def test_get_current_commute_work_home_status_1(create_user,app_test_context):
    '''
        Test getting commuted to work back when it is registered in the events table
    '''
    with app_test_context:
        # Get the user id
        userdata = create_user['info']
        user_id = userdata['users_id']
        
        event_obj = HandleEvents()
        # Set the date of the event happening
        this_date = datetime.datetime.now().strftime('%Y-%m-%d')
        # Make sure the default event types are registered
        event_obj.initialize_events()
        # Get event types
        work_at_home_event_type = event_obj.get_event_type("WorkFromHome")
        commute_event_type = event_obj.get_event_type("CommuteToWork")
        # Set the date
        the_date = datetime.datetime.now().strftime('%Y-%m-%d')
        # Register work at home
        toggle_status = event_obj.toggle_event(work_at_home_event_type,the_date,user_id)
        # Get the current commuted / worked at home status
        commute_status = event_obj.get_commute_status(user_id, the_date)
        assert commute_status == "WorkFromHome"

def test_get_current_commute_work_home_status_2(create_user,app_test_context):
    '''
        Test getting work from home back when it is registered in the events table
    '''
    with app_test_context:
        # Get the user id
        userdata = create_user['info']
        user_id = userdata['users_id']
        
        event_obj = HandleEvents()
        # Set the date of the event happening
        this_date = datetime.datetime.now().strftime('%Y-%m-%d')
        # Make sure the default event types are registered
        event_obj.initialize_events()
        # Get event types
        work_at_home_event_type = event_obj.get_event_type("WorkFromHome")
        commute_event_type = event_obj.get_event_type("CommuteToWork")
        # Set the date
        the_date = datetime.datetime.now().strftime('%Y-%m-%d')
        # Register commuted to work
        toggle_status = event_obj.toggle_event(commute_event_type,the_date,user_id)
        # Get the current commuted / worked at home status
        commute_status = event_obj.get_commute_status(user_id, the_date)
        assert commute_status == "CommuteToWork"

def test_get_current_commute_work_home_status_3(create_user,app_test_context):
    '''
        Test the return when neither work from home nor commute status is in the events table
    '''
    with app_test_context:
        # Get the user id
        userdata = create_user['info']
        user_id = userdata['users_id']
        
        event_obj = HandleEvents()
        # Set the date of the event happening
        this_date = datetime.datetime.now().strftime('%Y-%m-%d')
        # Make sure the default event types are registered
        event_obj.initialize_events()
        # Get event types
        work_at_home_event_type = event_obj.get_event_type("WorkFromHome")
        commute_event_type = event_obj.get_event_type("CommuteToWork")
        # Set the date
        the_date = datetime.datetime.now().strftime('%Y-%m-%d')
        # Get the current commuted / worked at home status
        commute_status = event_obj.get_commute_status(user_id, the_date)
        assert commute_status == None

def test_get_current_commute_work_home_status_4(create_user,app_test_context):
    '''
        Test to see False is returned when both event types are registered
        It is only allowed to have either work from home or commuted 
    '''
    with app_test_context:
        # Get the user id
        userdata = create_user['info']
        user_id = userdata['users_id']
        
        event_obj = HandleEvents()
        # Set the date of the event happening
        this_date = datetime.datetime.now().strftime('%Y-%m-%d')
        # Make sure the default event types are registered
        event_obj.initialize_events()
        # Get event types
        work_at_home_event_type = event_obj.get_event_type("WorkFromHome")
        commute_event_type = event_obj.get_event_type("CommuteToWork")
        # Set the date
        the_date = datetime.datetime.now().strftime('%Y-%m-%d')
        # Register BOTH event types
        toggle_status = event_obj.toggle_event(commute_event_type,the_date,user_id)
        toggle_status = event_obj.toggle_event(work_at_home_event_type,the_date,user_id)
        # Get the current commuted / worked at home status - we should get False
        # since this is not allowed
        commute_status = event_obj.get_commute_status(user_id, the_date)
        assert commute_status == False

def test_get_time_registered_today(create_user, app_test_context):
    '''
        Test retrieving the time registered on a given date
    '''
    # Get the user id
    userdata = create_user['info']
    user_id = userdata['users_id']
    tu = TestUtils()
    time_reg = TimeRegistration(user_id)
    with app_test_context:
        # Create an activity on which to register some time
        activity_name_str = tu.createRandomString()
        activity_uuid = time_reg.add_activity(activity_name_str)
        # Establish the start time and date for the reigstration
        start_timefrom = datetime.datetime.now()
        thisdate = start_timefrom.strftime('%Y-%m-%d')
        # Base timestamps
        timefrom_timestamp = start_timefrom
        timeto_timestamp = timefrom_timestamp + datetime.timedelta(minutes=2)
        # hour and minute times of first entry
        timefrom1 = timefrom_timestamp.strftime('%I:%M')
        timeto1 = timeto_timestamp.strftime('%I:%M')
        # Timestamps for 2nd entry
        timefrom2_timestamp = timeto_timestamp
        timeto2_timestamp = timefrom2_timestamp + datetime.timedelta(minutes=2)
        # Hour and minute times of 2nd entry
        timefrom2 = timefrom2_timestamp.strftime('%I:%M')
        timeto2 = timeto2_timestamp.strftime('%I:%M')
        time_reg.add_timeregistration(activity_uuid,thisdate,timefrom1,timeto1,testing=True)
        time_reg.add_timeregistration(activity_uuid,thisdate,timefrom2,timeto2,testing=True)
        
        # 4 minutes have been registered. Let's get the time out from the db again
        time_registered = time_reg.get_registration_time_on_day(thisdate)
        assert time_registered == "00:04"

def test_find_hours_current_week(create_user):
    '''
        Test we can get the start and end date for a week
    '''
    # March 1st is a good candidate to test out date calculation
    # since february is a short month
    the_date = "2022-03-01"
    date_utils = DoTimeDataHelp()
    start_of_week, end_of_week = date_utils.get_start_end_of_week(the_date)
    assert str(start_of_week) == "2022-02-28"
    assert str(end_of_week) == "2022-03-06"

def test_get_time_registered_this_week(create_user, app_test_context):
    '''
        Test retrieving the time registered on a given date
    '''
    # Get the user id
    userdata = create_user['info']
    user_id = userdata['users_id']
    tu = TestUtils()
    time_reg = TimeRegistration(user_id)
    date_util = DoTimeDataHelp()
    with app_test_context:
        # Create an activity on which to register some time
        activity_name_str = tu.createRandomString()
        activity_uuid = time_reg.add_activity(activity_name_str)
        # Establish the start time and date for the reigstration
        start_timefrom = datetime.datetime.now()
        start_of_week,end_of_week = date_util.get_start_end_of_week(start_timefrom.strftime('%Y-%m-%d'))
        day_1 = start_of_week
        # Base timestamps - Monday worked 1 hour
        timefrom_timestamp = datetime.datetime.strptime(day_1,'%Y-%m-%d')
        timeto_timestamp = timefrom_timestamp + datetime.timedelta(minutes=60)
        # hour and minute times of first entry 
        timefrom1 = timefrom_timestamp.strftime('%H:%M')
        timeto1 = timeto_timestamp.strftime('%H:%M')
        # Timestamps for 2nd entry - 1 hour worked on tuesday
        timefrom2_timestamp = timeto_timestamp + datetime.timedelta(days=1)
        timeto2_timestamp = timefrom2_timestamp + datetime.timedelta(minutes=60)
        day_2 = timefrom2_timestamp.strftime('%Y-%m-%d')
        # Hour and minute times of 2nd entry
        timefrom2 = timefrom2_timestamp.strftime('%H:%M')
        timeto2 = timeto2_timestamp.strftime('%H:%M')
        time_reg.add_timeregistration(activity_uuid,day_1,timefrom1,timeto1,testing=True)
        time_reg.add_timeregistration(activity_uuid,day_2,timefrom2,timeto2,testing=True)
        
        # 4 minutes have been registered. Let's get the time out from the db again
        time_registered = time_reg.get_registration_time_for_week(day_1)
        assert time_registered == "02:00"

def test_converting_minutes_to_hour_1():
    '''
        Test minutes over 60 getting converted to hours
    '''
    minutes = 85
    dotime_help = DoTimeDataHelp()
    hours,minutes = dotime_help.convert_minutes_to_hours(minutes)
    assert minutes == 25
    assert hours == 1

def test_converting_minutes_to_hour_2():
    '''
        Test minutes over 60 getting converted to hours
    '''
    minutes = 374
    dotime_help = DoTimeDataHelp()
    hours,minutes = dotime_help.convert_minutes_to_hours(minutes)
    assert minutes == 14
    assert hours == 6

def test_minutes_over_60_converted_to_hours_when_getting_time_for_week(create_user, app_test_context):
    '''
        Test minutes are converted to hours when getting total time registered for a week
    '''
    # Get the user id
    userdata = create_user['info']
    user_id = userdata['users_id']
    tu = TestUtils()
    time_reg = TimeRegistration(user_id)
    date_util = DoTimeDataHelp()
    with app_test_context:
        # Create an activity on which to register some time
        activity_name_str = tu.createRandomString()
        activity_uuid = time_reg.add_activity(activity_name_str)
        # Establish the start time and date for the reigstration
        start_timefrom = datetime.datetime.now()
        start_of_week,end_of_week = date_util.get_start_end_of_week(start_timefrom.strftime('%Y-%m-%d'))
        day_1 = start_of_week
        # Base timestamps - Monday worked 37 minutes hour
        timefrom_timestamp = datetime.datetime.strptime(day_1,'%Y-%m-%d')
        timeto_timestamp = timefrom_timestamp + datetime.timedelta(minutes=37)
        # hour and minute times of first entry 
        timefrom1 = timefrom_timestamp.strftime('%H:%M')
        timeto1 = timeto_timestamp.strftime('%H:%M')
        # Timestamps for 2nd entry - 33 minutes worked on tuesday
        timefrom2_timestamp = timeto_timestamp + datetime.timedelta(days=1)
        timeto2_timestamp = timefrom2_timestamp + datetime.timedelta(minutes=33)
        day_2 = timefrom2_timestamp.strftime('%Y-%m-%d')
        # Hour and minute times of 2nd entry
        timefrom2 = timefrom2_timestamp.strftime('%H:%M')
        timeto2 = timeto2_timestamp.strftime('%H:%M')
        # Timestamps for 3rd entry - 21 minutes worked on wednesday
        timefrom3_timestamp = timeto2_timestamp + datetime.timedelta(days=1)
        timeto3_timestamp = timefrom3_timestamp + datetime.timedelta(minutes=21)
        day_3 = timefrom2_timestamp.strftime('%Y-%m-%d')
        # Hour and minute times of 2nd entry
        timefrom3 = timefrom3_timestamp.strftime('%H:%M')
        timeto3 = timeto3_timestamp.strftime('%H:%M')
        time_reg.add_timeregistration(activity_uuid,day_1,timefrom1,timeto1,testing=True)
        time_reg.add_timeregistration(activity_uuid,day_2,timefrom2,timeto2,testing=True)
        time_reg.add_timeregistration(activity_uuid,day_3,timefrom3,timeto3,testing=True)
        
        # 4 minutes have been registered. Let's get the time out from the db again
        time_registered = time_reg.get_registration_time_for_week(day_1)
        assert time_registered == "01:31"
