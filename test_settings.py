'''Test handling of settings for the users'''
from app.profile.settings import SettingsHandling
from test_utils import TestUtils
import pytest

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
