"""Test profile handling"""

from werkzeug.security import check_password_hash
from ..profile.profile import ProfileHandling
from ..profile.settings import SettingsHandling
from .test_utils import TestUtils
from dotime.tests.conftest import create_profile


def test_generate_password():
    """Test a password can be created, and then validated by werkzeug check_password_hash function"""
    prof = ProfileHandling()
    tu = TestUtils()
    password = tu.createRandomString()
    hashed_password = prof.create_password(password)
    assert check_password_hash(hashed_password, password)


def test_password_check():
    """Checking to see a generated password can be validated"""
    prof = ProfileHandling()
    tu = TestUtils()
    password = tu.createRandomString()
    hashed_password = prof.create_password(password)
    assert prof.validate_password(hashed_password, password)


def test_add_user():
    """Test adding a user"""
    tu = TestUtils()
    username = tu.createRandomString()
    password = tu.createRandomString()
    email = tu.createRandomEmail()
    prof = ProfileHandling()
    user_id = prof.add_user(username, password, email)
    assert isinstance(user_id, dict)


def test_check_password():
    """Test methods behind a user login"""
    tu = TestUtils()
    username = tu.createRandomString()
    password = tu.createRandomString()
    email = tu.createRandomEmail()
    prof = ProfileHandling()
    user_id = prof.add_user(username, password, email)
    assert isinstance(user_id, dict)
    # Now check the methods behind the user login
    prof = ProfileHandling()
    user_id = prof.check_credentials(email, password)
    assert user_id is not None


def test_retrieve_profile_data():
    """Test getting profile data"""
    prof = ProfileHandling()
    tu = TestUtils()
    username = tu.createRandomString()
    password = tu.createRandomString()
    email = tu.createRandomEmail()
    prof = ProfileHandling()
    user_id = prof.add_user(username, password, email)
    userdata = prof.get_user_data(user_id.get("users_id"))
    assert username == userdata["username"]
    assert email == userdata["email"]


def test_edit_profile_data(app_test_context):
    """Test email address can be changed on a profile"""
    with app_test_context:
        prof = ProfileHandling
        tu = TestUtils()
        username = tu.createRandomString()
        password = tu.createRandomString()
        email = tu.createRandomEmail()
        prof = ProfileHandling()
        user_id = prof.add_user(username, password, email)
        new_email = tu.createRandomEmail()
        update_succeeded = prof.update_profile(
            users_id=user_id.get("users_id"), email=new_email
        )
        assert update_succeeded is True
        userdata = prof.get_user_data(user_id.get("users_id"))
        assert userdata["email"] == new_email


def test_update_password(create_user):
    tu = TestUtils()
    prof = ProfileHandling()
    new_password = tu.createRandomString()
    username = tu.createRandomString()
    password = tu.createRandomString()
    email = tu.createRandomEmail()
    prof = ProfileHandling()
    user_info = prof.add_user(username, password, email)

    password_updated = prof.update_password(
        user_info["users_id"], user_info["email"], password, new_password
    )
    assert password_updated is True


def test_get_email_by_uuid(create_user):
    """Look up a users email addresse by uuid"""
    user_id = create_user["info"]
    prof = ProfileHandling()
    email = prof.get_email_by_uuid(user_id["users_id"])
    assert email == create_user["email"]


def test_get_uuid_by_email(create_user):
    """Look up an uuid by providing an email"""
    userdata = create_user["info"]
    users_id = userdata["users_id"]
    email = userdata["email"]
    prof = ProfileHandling()
    assert users_id == prof.get_uuid_by_email(email)


def test_defaults_added_when_profile_created(client):
    """Test if default settings are added upon profile creation"""
    tu = TestUtils()
    email = tu.createRandomEmail()
    password = tu.createRandomString()
    username = tu.createRandomString()
    create_profile(client, username, email, password)
    settings_obj = SettingsHandling()
    prof = ProfileHandling()
    users_id = prof.get_uuid_by_email(email)
    settings = settings_obj.get_settings(users_id)
    # 2 settings for each workday should be registered.
    # As a settings is added for hour and minute count for each workday
    assert len(settings) == 14
