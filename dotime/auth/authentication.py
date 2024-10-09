"""Class for authentication"""

import functools
from psycopg2 import DatabaseError
from flask import current_app, redirect, url_for, g, request
from dotime.db import database


class Authentication:
    # pylint: disable=too-few-public-methods
    """Class for handling authentication"""

    @classmethod
    def get_user_data(cls, uuid):
        """Retrieve user data by UUID"""
        db_obj = database.Database()
        conn = db_obj.connect()
        user = None
        with conn.cursor() as cursor:
            try:
                sql = f"SELECT username, email FROM soc.users \
                    WHERE usersid = '{uuid}'"
                cursor.execute(sql)
                if cursor.rowcount != 0:
                    user_data = cursor.fetchone()
                    user = {}
                    user["usersid"] = uuid
                    user["username"] = user_data[0]
                    user["email"] = user_data[1]
                else:
                    current_app.logger.info("No user found.")
                # logger.info(sql)
            except DatabaseError as error:
                # logger.error(error)
                current_app.logger.error(error)
            finally:
                conn.close()
        return user


def login_required(view):
    """Force login for endpoints, which require it"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth_blueprint.login", next=request.url))

        return view(**kwargs)

    return wrapped_view
