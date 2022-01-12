'''Class for authentication'''
from psycopg2 import DatabaseError
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
                #logger.info("select_user sql: %s",sql)
                cursor.execute(sql)
                if cursor.rowcount != 0:
                    user_data = cursor.fetchone()
                    user = {}
                    user['usersid'] = uuid
                    user['username'] = user_data[0]
                    user['email'] = user_data[1]
                    #logger.info("select_user found username: %s",user['username'])

                #logger.info(sql)
            except DatabaseError as error:
                #logger.error(error)
                print(error)
            finally:
                conn.close()
        return user
