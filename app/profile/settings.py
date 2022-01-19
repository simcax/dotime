'''Handling of settings for users'''
from psycopg2 import DatabaseError
from flask import current_app
from app.db.database import Database

class SettingsHandling:
    '''Class for handling sessions for users'''
    def add_setting(self, user_id, settingName, settingValue):
        '''Add a setting to the settings table'''
        setting_added = False
        try:
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                sql = f"INSERT INTO soc.userSettings (usersId, settingName, settingValue) \
                    VALUES ('{user_id}','{settingName}','{settingValue}')"
                cur.execute(sql)
                if cur.rowcount == 1:
                    conn.commit()
                    setting_added = True
        except DatabaseError as error:
            current_app.logger.error("Error executing sql: %s, error: %s", sql, error)
        finally:
            conn.close()
        return setting_added