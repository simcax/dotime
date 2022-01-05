'''Test the time registration page'''
import datetime
import pytest
from app import create_app

@pytest.fixture
def client():
    '''Client fixture'''
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        yield client

@pytest.fixture
def enter_time_form(client):
    '''Utliity to get the time entry form for registration of time'''
    return client.get("/time/enter")


def test_enter_time_endpoint_exists(client,enter_time_form):
    '''Test there is an endpoint which is called /time/enter'''
    rv = enter_time_form
    assert rv.status_code == 200

def test_enter_time_form(client, enter_time_form):
    '''Test a form exists on the endpoint for time registration entry'''
    rv = enter_time_form
    assert b"<form" in rv.data

def test_enter_time_form_action_endpoint(client,enter_time_form):
    '''Test the enter time form points to the correct endpoint'''
    rv = enter_time_form
    assert b'action="/time/register"' in rv.data

def test_enter_time_form_today_exists(client, enter_time_form):
    '''Test the current weekday is in the time entry form'''
    rv = enter_time_form
    today = datetime.datetime.now()
    year, weeknumber, weekday  = today.isocalendar()
    assert bytes(str(weeknumber), 'utf-8') in rv.data
