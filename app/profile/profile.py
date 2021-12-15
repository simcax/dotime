'''Class to handle new users'''
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2 import DatabaseError
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
                        return_value = users_id
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
