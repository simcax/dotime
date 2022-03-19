'''Handling of settings for users'''
from psycopg2 import DatabaseError,sql
from flask import current_app
from app.db.database import Database
from app.utils import date_utils

class SettingsHandling:
    '''Class for handling sessions for users'''

    @classmethod
    def add_setting(cls, user_id, setting_name, setting_value):
        '''Add a setting to the settings table'''
        setting_added = False
        try:
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                stmt = sql.SQL("""
                    INSERT INTO soc.userSettings (usersId, settingName, settingValue)
                    VALUES ({user_id},{setting_name},{setting_value})
                    ON CONFLICT (usersid,settingname)
                    DO UPDATE SET(settingname,settingvalue) = ({setting_name},{setting_value})
                """).format(
                    user_id = sql.Literal(user_id),
                    setting_name = sql.Literal(setting_name),
                    setting_value = sql.Literal(str(setting_value))
                )
                cur.execute(stmt)
                if cur.rowcount == 1:
                    conn.commit()
                    setting_added = True
                    current_app.logger.error("Settings updated with sql: %s", sql)
        except DatabaseError as error:
            current_app.logger.error("Error executing sql: %s, error: %s", sql, error)
        finally:
            conn.close()
        return setting_added

    def get_settings(self, user_id, as_dict=True):
        '''
            Retrieve all settings for a user
            If as_dict, will return a dictionary with the settings
        '''
        settings = {}
        try:
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                stmt = sql.SQL("""
                    SELECT settingName, settingValue FROM soc.userSettings
                    WHERE usersId = {user_id}
                """).format(
                    user_id = sql.Literal(user_id)
                )
                cur.execute(stmt)
                if cur.rowcount >= 1:
                    rows = cur.fetchall()
                    if as_dict:
                        settings = self.settings_to_dict(settings, rows)
                    else:
                        settings = rows
        except DatabaseError as error:
            current_app.logger.error("Error executing sql: %s, error: %s", sql, error)
        finally:
            conn.close()
        return settings

    @classmethod
    def settings_to_dict(cls, settings, rows):
        '''
            Converts rows list to dictionary
        '''
        for row in rows:
            this_setting = { row[0]: row[1]}
            settings.update(this_setting)
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
        # Add workday names to the mix
        from app.utils import date_utils
        datahelp = date_utils.DoTimeDataHelp()
        all_days = datahelp.all_days('en')
        for i in enumerate(all_days):
            workweek_day_lengths[f'workdayName{i[0]+1}'] = all_days[i[0]]
        return workweek_day_lengths

    def get_number_of_work_hours_for_a_week(self,user_id):
        '''
            Returns the total number of hours and minutes the user has as a standard work week
            This will be in the form of HH:MM - zero filled.
        '''
        date_util = date_utils.DoTimeDataHelp()
        work_week = self.get_workweek_day_lengths(user_id)
        total_hours_and_minutes = 0 
        hours = 0
        minutes = 0
        for key, value in work_week.items():
            if key.endswith('Hour'):
                hours += int(value)
            elif key.endswith('Minutes'):
                minutes += int(value)
        if minutes > 60:
            min_to_hours, min_to_remaining_minutes = date_util.convert_minutes_to_hours(minutes)
            hours = hours + min_to_hours
            minutes = min_to_remaining_minutes
        total_hours_and_minutes = f"{hours:02d}:{minutes:02d}"        

        return total_hours_and_minutes

    def get_number_of_work_hours_until_current_day(self,user_id,day_number):
        '''
            Takes a user_id and the daynumber as input
            Returning the intended number of hours, which should be worked as taken from the user settings
            The day number should be 1 = Monday, 2 = Tuesday, 3 = Wednesday, 4 = Thursday, 5 = Friday, 6 = Saturday, 7 = Sunday
            Return values will be hours and minutes: HH:MM - zerofilled
        '''
        date_util = date_utils.DoTimeDataHelp()
        work_week = self.get_workweek_day_lengths(user_id)
        total_hours_and_minutes = 0 
        hours = 0
        minutes = 0
        for i in range(0,day_number):
            hours += int(work_week.get(f'workdayLength{i+1}Hour'))
            minutes += int(work_week.get(f'workdayLength{i+1}Minutes'))
        if minutes >= 60:
            min_to_hours, min_to_remaining_minutes = date_util.convert_minutes_to_hours(minutes)
            hours = hours + min_to_hours
            minutes = min_to_remaining_minutes
        total_hours_and_minutes = f"{hours:02d}:{minutes:02d}"        

        return total_hours_and_minutes
