import pytest
from .test_utils import TestUtils
from app import create_app
from app.profile.profile import ProfileHandling
@pytest.fixture
def client():
    '''Client fixture'''
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        yield client

@pytest.fixture
def app_test_context():
    app = create_app('Testing')
    return app.app_context()

@pytest.fixture
def create_user():
    '''Provide a test user'''
    tu = TestUtils()
    user_details = {}
    user_details['username'] = tu.createRandomString()
    user_details['password'] = tu.createRandomString()
    user_details['email'] = tu.createRandomEmail()
    prof = ProfileHandling()
    user_details['info'] = prof.add_user(user_details['username'],user_details['password'],user_details['email'])
    return user_details

def create_profile(client,username,email,password):
    '''Helper function to call the createprofile endpoint with POST data'''
    return client.post('/profile/create',data=dict(
        profileUsername = username,
        profileEmail = email,
        profilePassword = password,
    ), follow_redirects = True)

def login(client,email,password):
    ''''Helper function to login a user'''
    return client.post('/auth/login', data=dict(
    email = email,
    password = password 
    ), follow_redirects = True)

def logout(client):
    return client.get('/auth/logout', follow_redirects=True)