'''Test time registration methods'''
import datetime
from venv import create
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

def test_add_timereg_overlapping_registrations(create_user):
    '''Tests an error will occour if a timeregistration overlaps another timeregistration'''
    time_reg = TimeRegistration(create_user['users_id'])
    tu = TestUtils()
    activity_name_str = tu.createRandomString()
    activity_uuid = time_reg.add_activity(activity_name_str)
    timefrom1 = datetime.datetime.now()
    timeto1 = timefrom1 + datetime.timedelta(minutes=2)
    timefrom2 = timefrom1 + datetime.timedelta(minutes=1)
    timeto2 = timefrom2 + datetime.timedelta(minutes=10)
    assert isinstance(activity_uuid, str)
    timereg_added_1 = time_reg.add_timeregistration(activity_uuid, timefrom1, timeto1)
    timereg_added_2 = time_reg.add_timeregistration(activity_uuid, timefrom2, timeto2)
    assert timereg_added_1 == True
    # Since the second timereg row overlaps with the first, insertion should fail.
    assert timereg_added_2 == False

def test_get_activities(create_user):
    tu = TestUtils()
    time_reg = TimeRegistration(create_user['users_id'])
    activity_name_str = tu.createRandomString()
    activity_uuid = time_reg.add_activity(activity_name_str)
    activity_name_str = tu.createRandomString()
    activity_uuid = time_reg.add_activity(activity_name_str)
    activites = time_reg.get_activites()
    assert len(activites) == 2
