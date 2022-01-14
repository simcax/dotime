'''Class to handle new users'''
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2 import DatabaseError
from flask import current_app
from app.db.database import Database
class ProfileHandling:
    '''Profile handling'''

    @classmethod
    def create_password(cls,password):
        '''Generate password hash'''
        return generate_password_hash(password)

    @classmethod
    def validate_password(cls,password_hash, password):
        '''Check the password hash (from the database) can validate against the given password'''
        return check_password_hash(password_hash, password)

    def add_user(self,username,password,email):
        '''Adds a new user to the database'''
        hashed_password = self.create_password(password)
        db_obj = Database()
        conn = db_obj.connect()
        return_value = False
        try:
            with conn.cursor() as cur:
                sql = f"INSERT INTO soc.users (username,email) \
                    VALUES ('{username}','{email}')\
                    RETURNING usersid"
                cur.execute(sql)
                users_id = cur.fetchone()[0]
                if users_id:
                    password_added = self.add_user_password(conn,users_id, hashed_password)
                    if password_added:
                        print(f"User got {users_id}")
                        user = { 'users_id': users_id, 'username': username, 'email': email}
                        return_value = user
                        conn.commit()
                    else:
                        print(f"User {users_id} 's password failed to be added.\
                             Failing the user creation.")
                        return_value = False
                else:
                    print("User not added")
                    return_value = False

        except DatabaseError as error:
            print(f'Problem performing sql: {sql} - error: {error}')
        finally:
            conn.close()
        return return_value

    @classmethod
    def add_user_password(cls, conn, user_id, password_hash):
        '''Add a users password hash to the password table'''
        return_value = False
        try:
            with conn.cursor() as cur:
                sql = f"INSERT INTO soc.userpasswords (usersid, passwordhash)\
                     VALUES ('{user_id}','{password_hash}')"
                cur.execute(sql)
                conn.commit()
                return_value = bool(cur.rowcount)
        except DatabaseError as error:
            print(f'Problem performing sql: {sql} - error: {error}')
        return return_value

    def check_credentials(self,email,password):
        '''Authenticate user against the users and passwords tables'''
        try:
            db_obj = Database()
            conn = db_obj.connect()
            users_id = None
            with conn.cursor() as cur:
                sql = f"SELECT u.usersid, p.passwordHash FROM soc.users u \
                    INNER JOIN soc.userpasswords p ON u.usersid = p.usersid \
                    WHERE u.email = '{email}'"
                cur.execute(sql)
                if cur.rowcount >= 1:
                    row = cur.fetchone()
                    if self.validate_password(row[1],password):
                        users_id = row[0]
        except DatabaseError as error:
            print(f"Problem performing sql: {sql} - Error: {error}")
        finally:
            conn.close()
        return users_id

    def get_user_data(self,user_id):
        '''Retrieves a users profile data'''
        return_value = False
        try:
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                sql = f"SELECT username, email FROM soc.users \
                        WHERE usersid = '{user_id}'\
                    "
                cur.execute(sql)
                if cur.rowcount >= 1:
                    row = cur.fetchone()
                    userdata = { 'username': row[0], 'email': row[1]}
                    return_value = userdata
        except DatabaseError as error:
            current_app.logger.error("Problem running sql %s, error: %s", sql, error)
        finally:
            conn.close()
        return return_value

    def update_profile(self,users_id, email):
        '''Updates the email address on a profile by uuid'''
        updated = False
        try:
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                sql = f"UPDATE soc.users \
                    SET email = '{email}' \
                    WHERE usersid = '{users_id}'"
                cur.execute(sql)
                updated = bool( cur.rowcount == 1)
                if updated:
                    current_app.logger.info("userid %s updated", users_id)
                    conn.commit()
                else:
                    current_app.logger.warning("userid %s was not updated", users_id)
        except DatabaseError as error:
            current_app.logger.error("Problem running sql %s, error: %s", sql, error)
        finally:
            conn.close()
        return updated