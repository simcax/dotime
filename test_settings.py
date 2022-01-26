
'''Test handling of settings for the users'''
from venv import create
import pytest
from conftest import login, logout
from app.profile.settings import SettingsHandling
from app.db import database
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

def test_set_defaults_on_no_settings(create_user, app_test_context):
    '''Tests adding sane default settings to a user, if there are no settings'''
    with app_test_context:
        settings = SettingsHandling()
        userdata = create_user['user_id']
        user_id = userdata['users_id']
        user_settings = settings.get_settings(user_id)
        assert len(user_settings) == 0
        settings.add_defaults(user_id)
        user_settings_2 = settings.get_settings(user_id)
        assert len(user_settings_2) == 14
    
def test_get_workday_defaults(create_user, app_test_context):
    '''Test retrieving settings about the defaults for a work week'''
    with app_test_context:
        settings = SettingsHandling()
        userdata = create_user['user_id']
        user_id = userdata['users_id']
        # Make sure we have added default workday lengths to the users profile
        settings.add_defaults(user_id)
        user_settings = settings.get_settings(user_id)
        # Retrieve an object with the lenght of all the workdays.
        # This should be for Monday through Sunday.
        # The method should add any missing days with a 0 hours and 0 minutes
        workweek_day_lengths = settings.get_workweek_day_lengths(user_id)
        for i in range(1,8):
            assert workweek_day_lengths.get(f"workdayLength{i}Hour", 'empty') != 'empty'
            assert workweek_day_lengths.get(f"workdayLength{i}Minutes", 'empty') != 'empty'

def test_inserting_duplicate_settings_for_user(create_user,app_test_context):
    '''Test a setting will be updated when adding a setting already in the settings table'''
    with app_test_context:
        tu = TestUtils()
        setting_name = tu.createRandomString()
        setting_value = tu.createRandomString()
        settings = SettingsHandling()
        userdata = create_user['user_id']
        user_id = userdata['users_id']
        # Add setting to user
        settings_added = settings.add_setting(user_id,setting_name,setting_value)
        # Add setting again
        settings_added_2 = settings.add_setting(user_id,setting_name,setting_value)
        # Retrieve settings
        user_settings = settings.get_settings(user_id,as_dict=False)
        # We should only have 1 setting
        assert len(user_settings) == 1

def test_updating_value_to_zero(create_user,app_test_context):
    '''Test a setting will be updated when adding a setting already in the settings table'''
    with app_test_context:
        tu = TestUtils()
        setting_name = tu.createRandomString()
        setting_value = "0"
        settings = SettingsHandling()
        userdata = create_user['user_id']
        user_id = userdata['users_id']
        # Add setting to user with value 0
        settings_added = settings.add_setting(user_id,setting_name,setting_value)
        # Retrieve settings
        user_settings = settings.get_settings(user_id,as_dict=True)
        # The value of the setting should be 0
        assert user_settings.get(setting_name) == setting_value