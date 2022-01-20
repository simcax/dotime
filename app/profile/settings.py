'''Handling of settings for users'''
from psycopg2 import DatabaseError
from flask import current_app
from app.db.database import Database

class SettingsHandling:
    '''Class for handling sessions for users'''
    def add_setting(self, user_id, setting_name, setting_value):
        '''Add a setting to the settings table'''
        setting_added = False
        try:
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                sql = f"INSERT INTO soc.userSettings (usersId, settingName, settingValue) \
                    VALUES ('{user_id}','{setting_name}','{setting_value}')"
                cur.execute(sql)
                if cur.rowcount == 1:
                    conn.commit()
                    setting_added = True
        except DatabaseError as error:
            current_app.logger.error("Error executing sql: %s, error: %s", sql, error)
        finally:
            conn.close()
        return setting_added

    def get_settings(self, user_id):
        '''Retrieve all settings for a user'''
        settings = {}
        try:
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                sql = f"SELECT settingName, settingValue FROM soc.userSettings\
                    WHERE usersId = '{user_id}'"
                cur.execute(sql)
                if cur.rowcount >= 1:
                    rows = cur.fetchall()
                    for row in rows:
                        this_setting = { row[0]: row[1]}
                        settings.update(this_setting)
        except DatabaseError as error:
            current_app.logger.error("Error executing sql: %s, error: %s", sql, error)
        finally:
            conn.close()
        return settings

    def add_defaults(self,user_id):
        '''Add sane defaults to users profile'''
        standard_workday_hours = 7
        standard_workday_minutes = 30
        # By default we consider a normal working week to be monday to friday
        default_settings_added = False
        for i in range(1,8):
            # Let's add Monday to Friday with default hours
            # And weekends as zero hours
            if i < 6:
                hours = standard_workday_hours
                minutes = standard_workday_minutes
            else:
                hours = 0
                minutes = 0
            # Define the standard hour count for a day
            settings_name = f"workdayLength{i}Hour"
            settings_value = hours
            # Add standard hours for the day
            hour_setting_added = self.add_setting(user_id,settings_name, settings_value)


            # Define the standard minutes count for a day
            settings_name = f"workdayLength{i}Minutes"
            settings_value = minutes
            # Add standard minutes count to the settings table for the day
            minutes_setting_added = self.add_setting(user_id,settings_name,settings_value)
            if minutes_setting_added and hour_setting_added:
                default_settings_added = True
                continue
            else:
                break
        return default_settings_added

    def get_workweek_day_lengths(self,user_id):
        '''Get the profiles settings for the workweek'''
        settings = self.get_settings(user_id)
        workweek_day_lengths = {k: v for k, v in settings.items() if k.startswith('workdayLength')}
        return workweek_day_lengths
