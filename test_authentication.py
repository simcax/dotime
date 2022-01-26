''''Test authentication methods'''
import pytest
from conftest import app_test_context
from test_utils import TestUtils
from app.profile.profile import ProfileHandling
from app.auth import authentication

def test_get_user_by_uuid(app_test_context):
    '''Test getting user data by uuid'''    
    with app_test_context:
        tu = TestUtils()
        username = tu.createRandomString()
        password = tu.createRandomString()
        email = tu.createRandomEmail()
        prof = ProfileHandling()
        user_id = prof.add_user(username,password,email)
        auth = authentication.Authentication()
        user_data = auth.get_user_data(user_id['users_id'])
    assert user_data['username'] == username
    assert user_data['email'] == email

def test_redirect_to_login_on_unauthorized_endpoint(client):
    rv = client.get("/auth/unauthorized")
    assert rv.status_code == 302
    assert "/auth/login" in rv.location

def login(client,email,password):
    ''''Helper function to login a user'''
    return client.post('/auth/login', data=dict(
    email = email,
    password = password 
    ), follow_redirects = True)

# def test_authorized_endpoint_after_login(client, create_user):
#     login(client, create_user['email'], create_user['password'])
#     rv = client.get("/auth/unauthorized")
#     assert rv.status_code == 200