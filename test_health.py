''''Testing the health class'''
from app.health.health import Health

def test_db_connection():
    '''Tests the method for testing the database connection'''
    h_obj = Health()
    connection_test = h_obj.check_db()
    assert connection_test == True

def test_db_user_check():
    '''Tests the method for counting number of users (making sure a user table exists)'''
    h_obj = Health()
    user_test = h_obj.get_user_count()
    assert isinstance(user_test,int)
