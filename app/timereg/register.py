'''Module handling time registration'''
from psycopg2 import DatabaseError
from app.db import database

class TimeRegistration:
    '''Class for time registration'''

    def __init__(self,userid) -> None:
        self.userid = userid

    def add_activity(self,activity_name):
        '''Adds an activity to the activity table'''
        activity_uuid = False
        try:
            db = database.Database()
            conn = db.connect()
            with conn.cursor() as cur:
                sql = f"INSERT INTO soc.activites (usersId,activityname) \
                VALUES ('{self.userid}','{activity_name}') RETURNING activitesuuid"
                cur.execute(sql)
                activity_uuid = cur.fetchone()[0]
                conn.commit()
        except DatabaseError as error:
            print(f"Error with sql {sql} - {error}")
        finally:
            # Close connection
            conn.close()
        return activity_uuid
