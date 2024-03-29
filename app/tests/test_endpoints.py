'''Test the app endpoints'''
from datetime import date
import os
import pytest
from app import create_app
from .test_utils import TestUtils
from app.profile.profile import ProfileHandling

@pytest.fixture
def client():
    '''Client fixture'''
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        yield client

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

def test_create_profile_1(client,app_test_context):

    tu = TestUtils()
    username = tu.createRandomString()
    password = tu.createRandomString()
    email = tu.createRandomEmail()
    rv = create_profile(client, username, email, password)
    assert b'login' in rv.data

def test_create_profile_2(client):
    '''Testing the profile creation fails, if the user already exists'''
    tu = TestUtils()
    username = tu.createRandomString()
    password = tu.createRandomString()
    email = tu.createRandomEmail()
    rv = create_profile(client, username, email, password)
    assert b'login' in rv.data
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

# This needs to be figured out - how do we test for login, when the test client doesn't work 
# with cookies? Maybe move to selenium testing?
# def test_login(client,create_user):
#     '''Test a user can login'''
#     rv = login(client,create_user['email'],create_user['password'])
#     assert rv.status_code == 200
#     assert b"You are logged in." in rv.data

def test_loggedin_user_info_endpoint(client):
    '''Test the user info endpoint exists'''
    rv = client.get("/profile/info")
    assert rv.status_code == 200

def test_login_session_var_set(client, create_user):
    '''Test a user is logged in and session variables are set accordingly'''
    rv = login(client,create_user['email'],create_user['password'])
    assert client.get("/user/info")

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

def test_welcome_jpg(client):
    rv = client.get("/images/welcome.jpg")
    assert rv.status_code == 200

def test_set_session_value(client):
    '''Test the set session value endpoint exists and can take a value parameter'''
    tu = TestUtils()
    set_value = tu.createRandomString()
    rv = client.get(f"/session/set?value={set_value}")
    assert rv.status_code == 200
    return_string = f"Session value set to: {set_value}"
    assert bytes(return_string,'utf-8') in rv.data

def test_get_session_value(client):
    '''Test the set session value endpoint exists and it sets a session variable'''
    tu = TestUtils()
    set_value = tu.createRandomString()
    rv = client.get(f'/session/set?value={set_value}')
    rv2 = client.get('/session/getTest')
    assert bytes(set_value,'utf-8') in rv.data

def test_get_cookie(client, create_user):
    rv = login(client,create_user['email'],create_user['password'])
    assert rv.status_code == 200
    cookie_headers = rv.headers['set-cookie']
    # Make sure a cookie with the name DoTime is in the header
    assert 'DoTime=' in cookie_headers

def test_cookie_flags_1(client, create_user):
    rv = login(client,create_user['email'],create_user['password'])
    assert rv.status_code == 200
    cookie_headers = rv.headers['set-cookie']
    # Make sure a cookie with the name DoTime is in the header
    assert 'HttpOnly' in cookie_headers

def test_cookie_flags_2(client, create_user):
    rv = login(client,create_user['email'],create_user['password'])
    assert rv.status_code == 200
    cookie_headers = rv.headers['set-cookie']
    # Make sure a cookie with the name DoTime is in the header
    assert 'Secure' in cookie_headers

def test_profile_endpoint(client):
    rv = client.get("/profile/me")
    assert rv.status_code == 302

def test_profile_endpoint_not_logged_in(client):
    '''
        Test we are being redirected to login when accessing the profile/me endpoint
        when we are not logged in
    '''
    rv = client.get("/profile/me")
    assert "/auth/login" in rv.location

# def test_profile_endpoint_update_profile_exists(client):
#     '''Test the update profile endpoint exists'''
#     rv = client.post("/profile/update")
#     assert rv.status_code == 200

# def test_profile_endpoint_update_profile_1(client,create_user):
#     '''Tests updating the email address on a profile'''
#     login(client,create_user['email'],create_user['password'])
#     tu = TestUtils()
#     new_email = tu.createRandomEmail()
#     rv = client.post("/profile/update", data=dict( new_email = new_email))
#     assert b"Profile updated" in rv.data

def test_profile_change_password_form_exists(client):
    '''Test an endpoint exist for the update password form'''
    rv = client.get("/profile/changePassword")
    assert rv.status_code == 302

def test_profile_change_password_form_exists(client,create_user):
    '''Test an endpoint exist for the update password form'''
    rv = login(client,create_user['email'],create_user['password'])
    rv = client.get("/profile/changePassword")
    assert rv.status_code == 302

def test_profile_settings_endpoint_is_protected(client):
    '''Test the /profile/settings endpoint exists and is protected'''
    rv = client.get("/profile/settings")
    assert rv.status_code == 302

def test_frontpage_welcome_image(client):
    rv = client.get("/images/frontpage_welcome.jpg")
    assert rv.status_code == 200

def test_logo_image(client):
    rv = client.get("/images/dotime_logo.png")
    assert rv.status_code == 200

def test_favicon(client):
    rv = client.get("/favicon.ico")
    assert rv.status_code == 200

def test_datepicker_feature_image(client):
    rv = client.get("/images/datepicker_feature.png")
    assert rv.status_code == 200


    