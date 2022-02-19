'''Test time registration methods'''
import datetime
from datetime import date, time
from random import randint, choice
from venv import create
import uuid
import pytest
from app.timereg.register import TimeRegistration
from app.profile.profile import ProfileHandling
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