'''Test time registration methods'''
import datetime
import pytest
from app.timereg.register import TimeRegistration
from app.profile.profile import ProfileHandling
from test_utils import TestUtils

@pytest.fixture
def create_user():
    '''Provide a test user'''
    tu = TestUtils()
    username = tu.createRandomString()
    password = tu.createRandomString()
    email = tu.createRandomEmail()
    prof = ProfileHandling()
    user_details = prof.add_user(username,password,email)
    return user_details

def test_add_activity(create_user):
    '''Test an activity can be added to the activity table'''
    time_reg = TimeRegistration(create_user['users_id'])
    tu = TestUtils()
    activity_name_str = tu.createRandomString()
    activity_uuid = time_reg.add_activity(activity_name_str)
    assert isinstance(activity_uuid, str)

def test_add_timereg_row(create_user):
    '''Test adding a time registration row'''
    time_reg = TimeRegistration(create_user['users_id'])
    tu = TestUtils()
    activity_name_str = tu.createRandomString()
    activity_uuid = time_reg.add_activity(activity_name_str)
    timefrom = datetime.datetime.now()
    timeto = timefrom + datetime.timedelta(minutes=2)
    assert isinstance(activity_uuid, str)
    timereg_added = time_reg.add_timeregistration(activity_uuid, timefrom, timeto)
    assert timereg_added == True

def test_add_timereg_wrong_order(create_user):
    '''Test getting an error when adding a time reg record with to before from timestamp'''
    time_reg = TimeRegistration(create_user['users_id'])
    tu = TestUtils()
    activity_name_str = tu.createRandomString()
    activity_uuid = time_reg.add_activity(activity_name_str)
    timeto = datetime.datetime.now()
    timefrom = timeto + datetime.timedelta(minutes=2)
    assert isinstance(activity_uuid, str)
    timereg_added = time_reg.add_timeregistration(activity_uuid, timefrom, timeto)
    assert timereg_added == False

def test_add_timereg_correct_timestamps(create_user):
    '''Test a timestamp check is carried out when submitting a timereg entry'''
    time_reg = TimeRegistration(create_user['users_id'])
    tu = TestUtils()
    activity_name_str = tu.createRandomString()
    activity_uuid = time_reg.add_activity(activity_name_str)
    timefrom = datetime.datetime.now()
    timeto = str(timefrom + datetime.timedelta(minutes=2)) + "1a"
    assert isinstance(activity_uuid, str)
    timereg_added = time_reg.add_timeregistration(activity_uuid, timefrom, timeto)
    assert timereg_added == False