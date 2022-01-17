'''Test profile handling'''
from profile import Profile
import profile
import random
import string
from werkzeug.security import check_password_hash
from app.profile.profile import ProfileHandling
from test_utils import TestUtils

def test_generate_password():
    '''Test a password can be created, and then validated by werkzeug check_password_hash function'''
    prof = ProfileHandling()
    tu = TestUtils()
    password = tu.createRandomString()
    hashed_password = prof.create_password(password)
    assert check_password_hash(hashed_password,password)

def test_password_check():
    '''Checking to see a generated password can be validated'''
    prof = ProfileHandling()
    tu = TestUtils()
    password = tu.createRandomString()
    hashed_password = prof.create_password(password)
    assert prof.validate_password(hashed_password,password)

def test_add_user():
    '''Test adding a user'''
    tu = TestUtils()
    username = tu.createRandomString()
    password = tu.createRandomString()
    email = tu.createRandomEmail()
    prof = ProfileHandling()
    user_id = prof.add_user(username,password,email)
    assert isinstance(user_id,dict)

def test_check_password():
    '''Test methods behind a user login'''
    tu = TestUtils()
    username = tu.createRandomString()
    password = tu.createRandomString()
    email = tu.createRandomEmail()
    prof = ProfileHandling()
    user_id = prof.add_user(username,password,email)
    assert isinstance(user_id,dict)
    # Now check the methods behind the user login
    prof = ProfileHandling()
    user_id = prof.check_credentials(email,password)    
    assert user_id != None

def test_retrieve_profile_data():
    '''Test getting profile data'''
    prof = ProfileHandling()
    tu = TestUtils()
    username = tu.createRandomString()
    password = tu.createRandomString()
    email = tu.createRandomEmail()
    prof = ProfileHandling()
    user_id = prof.add_user(username,password,email)
    userdata = prof.get_user_data(user_id.get('users_id'))
    assert username == userdata['username']
    assert email == userdata['email']

def test_edit_profile_data(app_test_context):
    '''Test email address can be changed on a profile'''
    with app_test_context:
        prof = ProfileHandling
        tu = TestUtils()
        username = tu.createRandomString()
        password = tu.createRandomString()
        email = tu.createRandomEmail()
        prof = ProfileHandling()
        user_id = prof.add_user(username,password,email)
        new_email = tu.createRandomEmail()
        update_succeeded = prof.update_profile(users_id=user_id.get('users_id'), email=new_email)
        assert update_succeeded == True
        userdata = prof.get_user_data(user_id.get('users_id'))
        assert userdata['email'] == new_email

def test_update_password(create_user):
    tu = TestUtils()
    prof = ProfileHandling()
    new_password = tu.createRandomString()
    username = tu.createRandomString()
    password = tu.createRandomString()
    email = tu.createRandomEmail()
    prof = ProfileHandling()
    user_info = prof.add_user(username,password,email)

    password_updated = prof.update_password(user_info['users_id'], user_info['email'], password,new_password)
    assert password_updated == True

def test_get_email_by_uuid(create_user):
    '''Look up a users email addresse by uuid'''
    user_id = create_user['user_id']
    prof = ProfileHandling()
    email = prof.get_email_by_uuid(user_id['users_id'])
    assert email == create_user['email']
