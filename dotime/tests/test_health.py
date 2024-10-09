"""'Testing the health class"""

from ..health.health import Health


def test_db_connection():
    """Tests the method for testing the database connection"""
    h_obj = Health()
    connection_test = h_obj.check_db()
    assert connection_test == True


def test_db_user_check():
    """Tests the method for counting number of users (making sure a user table exists)"""
    h_obj = Health()
    user_test = h_obj.get_user_count()
    assert isinstance(user_test, int)


def test_gimme_20():
    health = Health()
    my_result = health.gimme(20)
    assert my_result == 20


def test_gimme_20_wrong_input():
    health = Health()
    my_result = health.gimme("string")
    assert my_result == False
