'''Test the time registration page'''
import datetime
import pytest
from app import create_app
from app.utils import date_utils

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
    assert bytes(str(year), 'utf-8') in rv.data

def test_daynumber_to_dayname():
    '''Test conversion of daynumbers to daynames'''
    dotime_date_help = date_utils.DoTimeDataHelp()
    assert "Monday" == dotime_date_help.day_name('en',0)

def test_daynumber_to_dayname_unsupported():
    '''Test conversion of daynumbers to daynames for unsupported language'''
    dotime_date_help = date_utils.DoTimeDataHelp()
    assert "Language not supported" == dotime_date_help.day_name('us',0)

def test_daynumber_to_dayname_out_of_range():
    '''Test we get a sensible error when supplying a wrong daynumber'''
    dotime_date_help = date_utils.DoTimeDataHelp()
    assert "Daynumber out of range" == dotime_date_help.day_name('en',8)

def test_get_daynames():
    '''Test we get a list of daynames'''
    dotime_date_help = date_utils.DoTimeDataHelp()
    alldays = dotime_date_help.all_days('en')
    assert "Monday" in alldays
    assert "Tuesday" in alldays
    assert "Wednesday" in alldays
    assert "Thursday" in alldays
    assert "Friday" in alldays
    assert "Saturday" in alldays
    assert "Sunday" in alldays

def test_enter_time_form_input_field_for_day_exists(enter_time_form):
    rv = enter_time_form
    assert b'<input name="start"' in rv.data
