'''Class to handle new users'''
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2 import DatabaseError, sql
from flask import current_app, flash
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
                stmt = sql.SQL("""
                    INSERT INTO soc.users (username,email)
                    VALUES ({username},{email})
                    RETURNING usersid
                """).format(
                    username = sql.Literal(username),
                    email = sql.Literal(email)
                )
                cur.execute(stmt)
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
                stmt = sql.SQL("""
                    INSERT INTO soc.userpasswords (usersid, passwordhash)
                     VALUES ({user_id},{password_hash})
                    """).format(
                        user_id = sql.Literal(user_id),
                        password_hash = sql.Literal(password_hash)
                    )
                cur.execute(stmt)
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
                stmt = sql.SQL("""
                    SELECT u.usersid, p.passwordHash FROM soc.users u
                    INNER JOIN soc.userpasswords p ON u.usersid = p.usersid
                    WHERE u.email = {email}
                """).format(
                    email = sql.Literal(email)
                )
                cur.execute(stmt)
                if cur.rowcount >= 1:
                    row = cur.fetchone()
                    if self.validate_password(row[1],password):
                        users_id = row[0]
        except DatabaseError as error:
            print(f"Problem performing sql: {sql} - Error: {error}")
        finally:
            conn.close()
        return users_id

    @classmethod
    def get_user_data(cls,user_id):
        '''Retrieves a users profile data'''
        return_value = False
        try:
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                stmt = sql.SQL("""
                        SELECT username, email FROM soc.users
                        WHERE usersid = {user_id}
                    """).format(
                        user_id = sql.Literal(user_id)
                    )
                cur.execute(stmt)
                if cur.rowcount >= 1:
                    row = cur.fetchone()
                    userdata = { 'username': row[0], 'email': row[1]}
                    return_value = userdata
        except DatabaseError as error:
            current_app.logger.error("Problem running sql %s, error: %s", sql, error)
        finally:
            conn.close()
        return return_value

    @classmethod
    def update_profile(cls,users_id, email):
        '''Updates the email address on a profile by uuid'''
        updated = False
        try:
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                stmt = sql.SQL("""
                    UPDATE soc.users
                    SET email = {email}
                    WHERE usersid = {users_id}
                """).format(
                    email = sql.Literal(email),
                    users_id = sql.Literal(users_id)
                )
                cur.execute(stmt)
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

    def change_password(self,users_id, new_password):
        '''Method to change password for a user'''
        password_changed = False
        try:
            password_hash = self.create_password(new_password)
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                stmt = sql.SQL("""
                        UPDATE soc.userPasswords SET passwordHash = {password_hash}
                        WHERE usersid = {users_id}
                        """).format(
                            users_id = sql.Literal(users_id),
                            password_hash = sql.Literal(password_hash)
                        )
                cur.execute(stmt)
                password_changed = bool(cur.rowcount == 1)
                conn.commit()
        except DatabaseError as error:
            current_app.logger.error("Error during sql execution. Error: %s", error)
        finally:
            conn.close()
        return password_changed

    def update_password(self,users_id, email, current_password, new_password):
        '''Method to change password on a user'''
        if self.check_credentials(email,current_password) == users_id:
            password_changed = self.change_password(users_id, new_password)
        else:
            flash("Current password not correct")
            current_app.logger.warning("Users current password did not match")
            password_changed = False
        return password_changed

    @classmethod
    def get_email_by_uuid(cls, user_id):
        '''Method to get email by supplying uuid'''
        email = False
        try:
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                stmt = sql.SQL("""
                SELECT email FROM soc.users WHERE usersid = {user_id}
                """).format(
                    user_id = sql.Literal(user_id)
                )
                cur.execute(stmt)
                if cur.rowcount == 1:
                    email = cur.fetchone()[0]
        except DatabaseError as error:
            current_app.logger.error("Error performing sql query. SQL %s - error %s", sql, error)
        finally:
            conn.close()
        return email

    @classmethod
    def get_uuid_by_email(cls, email):
        '''Method to get user uuid by the given email'''
        uuid = False
        try:
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                stmt = sql.SQL("""
                    SELECT usersid FROM soc.users WHERE email = {email}
                """).format(
                    email = sql.Literal(email)
                )
                cur.execute(stmt)
                if cur.rowcount == 1:
                    uuid = cur.fetchone()[0]
        except DatabaseError as error:
            current_app.logger.error("Error performing sql query. SQL %s - error %s", sql, error)
        finally:
            conn.close()
        return uuid
