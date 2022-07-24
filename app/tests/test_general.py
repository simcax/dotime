import pytest
from os import environ
from ..app import create_app

@pytest.fixture
def client():
    '''Client fixture'''
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        yield client

def test_version_number_on_home(client):
    '''Test there is a version number on the fronpage'''
    environ['VERSION'] = "0.0.40"
    rv = client.get("/")
    assert b"Version: 0.0.40" in rv.data