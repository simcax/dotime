'''Test the app endpoints'''
import os
import pytest
from app import create_app
from test_utils import TestUtils
from app.profile.profile import ProfileHandling

@pytest.fixture
def client():
    '''Client fixture'''
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        yield client

@pytest.fixture
def create_user():
    '''Provide a test user'''
    tu = TestUtils()
    user_details = {}
    user_details['username'] = tu.createRandomString()
    user_details['password'] = tu.createRandomString()
    user_details['email'] = tu.createRandomEmail()
    prof = ProfileHandling()
    user_details['user_id'] = prof.add_user(user_details['username'],user_details['password'],user_details['email'])
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

def test_home_endpoint(client):
    ''''Test the home endpoint'''
    rv = client.get("/")
    assert b"Welcome to doTime" in rv.data

def test_create_profile_endpoint(client):
    '''Test the create profile endpoint'''
    rv = client.get("/profile/create")
    assert b'Create Profile' in rv.data

def test_create_profile_1(client):
    tu = TestUtils()
    username = tu.createRandomString()
    password = tu.createRandomString()
    email = tu.createRandomEmail()
    rv = create_profile(client, username, email, password)
    assert b'Your profile was created.' in rv.data

def test_create_profile_2(client):
    '''Testing the profile creation fails, if the user already exists'''
    tu = TestUtils()
    username = tu.createRandomString()
    password = tu.createRandomString()
    email = tu.createRandomEmail()
    rv = create_profile(client, username, email, password)
    assert b'Your profile was created.' in rv.data
    rv = create_profile(client,username, email, password)
    assert b"Sorry, we couldn't create your profile." in rv.data

def test_health_endpoint(client):
    ''''Testing the endpoint is defined'''
    rv = client.get("/health", follow_redirects=True)
    assert rv.status_code == 200

def test_login_endpoint(client):
    '''Testing the login endpoint exists and is reachable'''
    rv = client.get("/auth/login")
    assert rv.status_code == 200

def test_login(client,create_user):
    '''Test a user can login'''
    rv = login(client,create_user['email'],create_user['password'])
    assert rv.status_code == 200
    assert b"You are logged in." in rv.data

def test_login_fails(client,create_user):
    tu = TestUtils()
    random_string = tu.createRandomString()
    rv = login(client, create_user['email'],random_string)
    assert b"Error logging you in." in rv.data

def test_hello_jpg(client):
    rv = client.get("/images/hello.jpg")
    assert rv.status_code == 200

def test_oops_jpg(client):
    rv = client.get("/images/oops.jpg")
    assert rv.status_code == 200