'''Test the app endpoints'''
import os
import pytest
from app import create_app

@pytest.fixture
def client():
    '''Client fixture'''
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    ''''Test the home endpoint'''
    rv = client.get("/")
    assert b"Welcome to doTime" in rv.data

def test_create_profile_endpoint(client):
    '''Test the create profile endpoint'''
    rv = client.get("/profile/create")
    assert b'Create a profile' in rv.data