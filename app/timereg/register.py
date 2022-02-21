'''Module handling time registration'''
from uuid import UUID
from flask import current_app, flash
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

    def is_activityuuid(self, activity_uuid):
        '''
            Takes an activity_uuid and looks it up in the database. If the uuid exists for
            the user, true is returned, otherwise false
        '''
        is_activity_uuid = False
        if len(str(activity_uuid)) == 36:
            try:
                UUID(str(activity_uuid))
                try:
                    db_obj = database.Database()
                    conn = db_obj.connect()
                    with conn.cursor() as cur:
                        sql = f"SELECT 1 FROM soc.activites \
                                WHERE usersid = '{self.userid}' \
                                AND activitesuuid = '{activity_uuid}'"
                        cur.execute(sql)
                        is_activity_uuid = bool(cur.rowcount)
                except DatabaseError as error:
                    current_app.logger.error("Error executing sql: %s - error: %s",sql,error)
                finally:
                    conn.close()
            except ValueError:
                is_activity_uuid = False

        return is_activity_uuid

    def get_activites(self, activity_name=None, activity_uuid=None):
        '''Gets a list of unique activites from the database for the current user'''
        activities = {}
        and_activity_name = ""
        and_activity_uuid = ""
        if activity_name:
            and_activity_name = f"and activityname LIKE '%{activity_name}%'"
        if activity_uuid:
            and_activity_uuid = f"and activitesuuid = '{activity_uuid}'"
        try:
            db_obj = database.Database()
            conn = db_obj.connect()
            with conn.cursor(cursor_factory=DictCursor) as cur:
                sql = f"SELECT activitesuuid, activityname FROM soc.activites \
                        WHERE usersId = '{self.userid}' {and_activity_name} {and_activity_uuid}"
                current_app.logger.debug("%s",sql)
                cur.execute(sql)
                if cur.rowcount:
                    activities = cur.fetchall()
        except DatabaseError as error:
            current_app.logger.error("Error executing sql: %s - error: %s", sql, error)
        finally:
            conn.close()
        return activities

    @classmethod
    def create_select2_data_structure_for_ajax_call(cls,data,no_list=False):
        '''Creates the correct data structure for the select2 dropdown ajax call'''
        item_list = {}
        results = []
        if no_list:
            item_list = { 'id': data[0][0], 'text': data[0][1]}
        else:
            for uuid,activity_name in data:
                results_dict = {}
                results_dict['id'] = uuid
                results_dict['text'] = activity_name
                results.append(results_dict)

            item_list['results'] = results
        return item_list

    def add_timeregistration(self, activity_uuid, date, timefrom, timeto,testing=False):
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
                if not testing:
                    flash(f"Time period ({timefrom_full} or {timeto_full}) is already registered.")
                timereg_added = False
        else:
            if not testing:
                flash(f"Time from {timefrom} is after time to {timeto}")
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
            sql = f"SELECT 1 FROM soc.timedmeetgo WHERE timefrom <= '{timestamp}'  \
                AND timeto > '{timestamp}' AND usersid = '{self.userid}'"
            with conn.cursor() as cur:
                cur.execute(sql)
                timestamp_is_not_here = bool(cur.rowcount==0)
                if not timestamp_is_not_here:
                    current_app.logger.debug('Rows: %s - Timestamp %s existed already. SQL :%s'
                    ,cur.rowcount,timestamp, sql)
        except DatabaseError as error:
            print(f"Error executing SQL {sql} - {error}")
        finally:
            conn.close()
        return timestamp_is_not_here

    def get_registrations(self, registration_date):
        '''
            Get all timeregistration for a given date
        '''
        try:
            rows = False
            db_obj = database.Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                sql = f"SELECT experimental_strftime( t.timefrom,'%H:%M') as timefrom, \
                    experimental_strftime(t.timeto,'%H:%M') as timeto, \
                    a.activitesuuid, a.activityname \
                    FROM soc.timedmeetgo t \
                    INNER JOIN soc.ln_timemeetgo l ON t.timedmeetgouuid = l.timedmeetgouuid \
                    INNER JOIN soc.activites a ON l.activitesuuid = a.activitesuuid \
                    WHERE t.usersId = '{self.userid}' \
                    AND t.timefrom BETWEEN '{registration_date} 00:00:00' AND '{registration_date} 23:59:59' \
                    ORDER BY t.timefrom"
                current_app.logger.debug(sql)
                cur.execute(sql)
                rows = cur.fetchall()
        except DatabaseError as error:
            current_app.logger.error("Error executing sql: %s, error: %s", sql, error)
        finally:
            conn.close()
        return rows
