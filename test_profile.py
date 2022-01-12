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
    logged_in = prof.check_credentials(email,password)    
    assert logged_in == True
