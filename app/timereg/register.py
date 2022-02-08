'''Module handling time registration'''
from datetime import datetime
from time import strftime
from flask import current_app
from psycopg2 import DatabaseError
from psycopg2.extras import DictCursor
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
    
    def get_activites(self):
        '''Gets a list of unique activites from the database for the current user'''
        activities = {}
        try:
            db_obj = database.Database()
            conn = db_obj.connect()
            with conn.cursor(cursor_factory=DictCursor) as cur:
                sql = f"SELECT activitesuuid, activityname FROM soc.activites \
                        WHERE usersId = '{self.userid}'"
                cur.execute(sql)
                if cur.rowcount:
                    activities = cur.fetchall()
        except DatabaseError as error:
            current_app.logger.error("Error executing sql: %s - error: %s", sql, error)
        finally:
            conn.close()
        return activities

    def create_select2_data_structure_for_ajax_call(self,data):
        '''Creates the correct data structure for the select2 dropdown ajax call'''
        item_list = {}
        results = []
        results_dict = {}
        for uuid,activity_name in data:
            results_dict['id'] = uuid
            results_dict['text'] = activity_name
            results.append(results_dict)
        
        item_list['results'] = results
        return item_list

    def add_timeregistration(self, activity_uuid, date, timefrom, timeto):
        '''Adds a row to the time registration table with a link record to an activity uuid'''
        #datetime.datetime.strptime(timefrom, format)
        timereg_added = False
        if timefrom < timeto:
            timefrom_full = f"{date} {timefrom}"
            timeto_full = f"{date} {timeto}"

            if self.timestamp_is_not_registered(timefrom_full) and \
                self.timestamp_is_not_registered(timeto_full):
                try:
                    db_obj = database.Database()
                    conn = db_obj.connect()
                    with conn.cursor() as cur:
                        sql = f"INSERT INTO soc.timedmeetgo (timefrom, timeto, usersId) \
                            VALUES ('{timefrom_full}','{timeto_full}','{self.userid}') \
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
