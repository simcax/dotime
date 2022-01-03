'''Module handling time registration'''
from datetime import datetime
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
            db_obj = database.Database()
            conn = db_obj.connect()
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

    def add_timeregistration(self, activity_uuid, timefrom, timeto):
        '''Adds a row to the time registration table with a link record to an activity uuid'''
        timereg_added = False
        if isinstance(timefrom,datetime) and isinstance(timeto,datetime) and timefrom < timeto:
            if self.timestamp_is_not_registered(timefrom) and \
                self.timestamp_is_not_registered(timeto):
                try:
                    db_obj = database.Database()
                    conn = db_obj.connect()
                    with conn.cursor() as cur:
                        sql = f"INSERT INTO soc.timedmeetgo (timefrom, timeto, usersId) \
                            VALUES ('{timefrom}','{timeto}','{self.userid}') \
                                RETURNING timedmeetgouuid"
                        cur.execute(sql)
                        timed_meet_go_uuid = cur.fetchone()[0]

                        sql = f"INSERT INTO soc.ln_timemeetgo (timedmeetgouuid,activitesuuid) \
                            VALUES ('{timed_meet_go_uuid}','{activity_uuid}')"
                        cur.execute(sql)
                        if cur.rowcount == 1:
                            conn.commit()
                            timereg_added = True
                        else:
                            timereg_added = False
                except DatabaseError as error:
                    print(f"Error with sql {sql} - {error}")
                finally:
                    conn.close()
            else:
                timereg_added = False
        else:
            timereg_added = False
        return timereg_added

    def timestamp_is_not_registered(self, timestamp):
        '''
            Check if an existing registration exists,
            where the timeperiod would overlap with the given one
            Returns TRUE if the timestamp given does not exist for the user uuid
        '''
        try:
            timestamp_is_not_here = True
            db_obj = database.Database()
            conn = db_obj.connect()
            sql = f"SELECT 1 FROM soc.timedmeetgo WHERE timefrom <= '{timestamp}' \
                AND timeto >= '{timestamp}' AND usersid = '{self.userid}'"
            with conn.cursor() as cur:
                cur.execute(sql)
                timestamp_is_not_here = bool(cur.rowcount==0)
        except DatabaseError as error:
            print(f"Error executing SQL {sql} - {error}")
        finally:
            conn.close()
        return timestamp_is_not_here