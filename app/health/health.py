'''Implements health checking of the app'''
from psycopg2 import DatabaseError
from app.db.database import Database

class Health:
    '''yeilds methods to check the health of the app'''
    health_string = {}
    user_count = ''
    db_connection = ''

    def __init__(self):
        '''Initialize the class'''
        self.db_connection = self.check_db()
        self.user_count = self.get_user_count()
        self.health_string = { "dbConnection": self.db_connection, "userCount": self.user_count }

    def get_health_string(self):
        '''Returns the health status string'''
        return self.health_string

    @classmethod
    def check_db(cls):
        '''Check if we have database connection'''
        try:
            db_obj = Database()
            return_value = bool(db_obj.connect())
        except DatabaseError:
            return_value = False
        return return_value

    @classmethod
    def get_user_count(cls):
        '''Get number of users in the user table'''
        try:
            db_obj = Database()
            conn = db_obj.connect()
            if conn:
                with conn.cursor() as cursor:
                    sql = "SELECT COUNT(*) FROM soc.users"
                    print(sql)
                    cursor.execute(sql)
                    print(f"SQL {sql}")
                    user_count = cursor.fetchone()[0]
                    print(f"UserCount: {user_count}")
                    return_value = user_count
            else:
                return_value = "Database connection failed"
        except DatabaseError:
            return_value = False
        return return_value
