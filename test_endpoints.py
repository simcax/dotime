'''Test the app endpoints'''
import os
import pytest
from app import create_app
from test_utils import TestUtils

@pytest.fixture
def client():
    '''Client fixture'''
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        yield client

def createProfile(client,username,email,password):
    '''Helper function to call the createprofile endpoint with POST data'''
    return client.post('/profile/create',data=dict(
        profileUsername = username,
        profileEmail = email,
        profilePassword = password,
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
    rv = createProfile(client, username, email, password)
    assert b'Your profile was created!' in rv.data
