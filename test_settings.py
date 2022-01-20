
'''Test handling of settings for the users'''
from venv import create
import pytest
from conftest import login, logout
from app.profile.settings import SettingsHandling
from test_utils import TestUtils


def test_insert_data_to_setttings_table(create_user, app_test_context):
    with app_test_context:
        settings = SettingsHandling()
        tu = TestUtils
        settingName = tu.createRandomString()
        settingValue = tu.createRandomString()
        userdata = create_user['user_id']
        user_id = userdata['users_id']
        value_added = settings.add_setting(user_id,settingName, settingValue)
        assert value_added == True

def test_get_settings_for_user(create_user, app_test_context):
    with app_test_context:
        settings = SettingsHandling()
        tu = TestUtils
        settingName = tu.createRandomString()
        settingValue = tu.createRandomString()
        userdata = create_user['user_id']
        user_id = userdata['users_id']
        value_added = settings.add_setting(user_id,settingName, settingValue)
        assert value_added == True
        user_settings = settings.get_settings(user_id)
        assert len(user_settings) == 1

def test_get_settings_endpoint(client):
    '''Test the settings endpoint exists'''
    rv = client.get("/profile/settings")
    assert rv.status_code == 302

def test_set_defaults_on_no_settings(create_user):
    '''Tests adding sane default settings to a user, if there are no settings'''
    settings = SettingsHandling()
    userdata = create_user['user_id']
    user_id = userdata['users_id']
    user_settings = settings.get_settings(user_id)
    assert len(user_settings) == 0
    settings.add_defaults(user_id)
    user_settings_2 = settings.get_settings(user_id)
    assert len(user_settings_2) == 10
    
