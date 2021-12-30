'''Test time registration methods'''
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