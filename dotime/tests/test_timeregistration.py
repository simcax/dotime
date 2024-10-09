"""Test the time registration page"""

import datetime
import pytest
from . import test_utils
from dotime import create_app
from dotime.utils import date_utils


@pytest.fixture
def client():
    """Client fixture"""
    app = create_app({"TESTING": True})

    with app.test_client() as client:
        yield client


@pytest.fixture
def enter_time_form(client):
    """Utliity to get the time entry form for registration of time"""
    return client.get("/time/enter")


@pytest.fixture
def register_time_record_random(client, create_user):
    tu = test_utils.TestUtils()
    activity = tu.createRandomString()
    time_start = datetime.datetime.now()
    time_end = time_start + datetime.timedelta(minutes=1)
    time_date = time_start.strftime("%Y-%m-%d")
    time_start = time_start.strftime("%I:%M")
    time_end = time_end.strftime("%I:%M")
    user_data = create_user["info"]
    return register_time_record(
        client, activity, time_date, time_start, time_end, user_data["users_id"]
    )


def register_time_record(client, activity, time_date, time_start, time_end, user_id):
    """Utility method to send a time registration record to the endpoint"""
    return client.post(
        "/time/register",
        data=dict(
            timecode=activity,
            time_date=time_date,
            time_start=time_start,
            time_end=time_end,
            user_id=user_id,
        ),
        follow_redirects=True,
    )


def test_enter_time_endpoint_exists(client, enter_time_form):
    """Test there is an endpoint which is called /time/enter"""
    rv = enter_time_form
    assert rv.status_code == 200


def test_enter_time_form(client, enter_time_form):
    """Test a form exists on the endpoint for time registration entry"""
    rv = enter_time_form
    assert b"<form" in rv.data


def test_enter_time_form_action_endpoint(client, enter_time_form):
    """Test the enter time form points to the correct endpoint"""
    rv = enter_time_form
    assert b'action="/time/register"' in rv.data


def test_enter_time_form_today_exists(client, enter_time_form):
    """Test the current weekday is in the time entry form"""
    rv = enter_time_form
    today = datetime.datetime.now()
    year, weeknumber, weekday = today.isocalendar()
    assert bytes(str(year), "utf-8") in rv.data


def test_daynumber_to_dayname():
    """Test conversion of daynumbers to daynames"""
    dotime_date_help = date_utils.DoTimeDataHelp()
    assert "Monday" == dotime_date_help.day_name("en", 0)


def test_daynumber_to_dayname_unsupported():
    """Test conversion of daynumbers to daynames for unsupported language"""
    dotime_date_help = date_utils.DoTimeDataHelp()
    assert "Language not supported" == dotime_date_help.day_name("us", 0)


def test_daynumber_to_dayname_out_of_range():
    """Test we get a sensible error when supplying a wrong daynumber"""
    dotime_date_help = date_utils.DoTimeDataHelp()
    assert "Daynumber out of range" == dotime_date_help.day_name("en", 8)


def test_get_daynames():
    """Test we get a list of daynames"""
    dotime_date_help = date_utils.DoTimeDataHelp()
    alldays = dotime_date_help.all_days("en")
    assert "Monday" in alldays
    assert "Tuesday" in alldays
    assert "Wednesday" in alldays
    assert "Thursday" in alldays
    assert "Friday" in alldays
    assert "Saturday" in alldays
    assert "Sunday" in alldays


def test_enter_time_form_input_field_for_day_exists(enter_time_form):
    rv = enter_time_form
    assert b'<input name="time_start"' in rv.data


def test_enter_time_form_input_field_properties(enter_time_form):
    rv = enter_time_form
    assert b'<input name="time_start"' in rv.data
    assert b'<input name="time_end"' in rv.data


def test_time_register_endpoint_exists(client):
    rv = client.get("/time/register")
    assert rv.status_code == 302


# def test_time_register_entry(client,register_time_record_random,create_user):
#     from flask import session
#     userdata = create_user['info']
#     session['user_id'] = userdata.get('users_id')
#     rv = register_time_record_random
#     assert b"Time registration registered" in rv.data
