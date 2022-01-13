'''Class for authentication'''
import functools
from psycopg2 import DatabaseError
from flask import current_app, redirect, url_for, g
from app.db import database

class Authentication:
    '''Class for handling authentication'''
    def get_user_data(self,uuid):
        '''Retrieve user data by UUID'''
        db_obj = database.Database()
        conn = db_obj.connect()
        user = None
        with conn.cursor() as cursor:
            try:
                sql = f"SELECT username, email FROM soc.users \
                    WHERE usersid = '{uuid}'"
                current_app.logger.info("select_user sql: %s",sql)
                cursor.execute(sql)
                if cursor.rowcount != 0:
                    user_data = cursor.fetchone()
                    user = {}
                    user['usersid'] = uuid
                    user['username'] = user_data[0]
                    user['email'] = user_data[1]
                    current_app.logger.info("select_user found username: %s",user['username'])
                else:
                    current_app.logger.info("No user found.")
                #logger.info(sql)
            except DatabaseError as error:
                #logger.error(error)
                current_app.logger.error(error)
            finally:
                conn.close()
        return user

def login_required(view):
    '''Force login for endpoints, which require it'''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth_blueprint.login'))

        return view(**kwargs)

    return wrapped_view
