'''Test profile handling'''
from profile import Profile
import random
import string
from app.profile.profile import ProfileHandling
from werkzeug.security import check_password_hash

def createRandomString():
    ''''Helper function to create a random string - 10 chars long'''
    randomString = ''.join(random.choice(string.ascii_letters) for x in range(10))
    return randomString

def test_generate_password():
    '''Test a password can be created, and then validated by werkzeug check_password_hash function'''
    prof = ProfileHandling()
    password = createRandomString()
    hashed_password = prof.create_password(password)
    assert check_password_hash(hashed_password,password)

def test_password_check():
    '''Checking to see a generated password can be validated'''
    prof = ProfileHandling()
    password = createRandomString()
    hashed_password = prof.create_password(password)
    assert prof.validate_password(hashed_password,password)
