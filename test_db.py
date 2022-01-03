'''Test Database Class'''
import psycopg2
from app.db.database import Database

def test_db_initialization():
    db = Database()
    assert db.db_connection_string is not None

def test_db_connection():
    db = Database()
    conn = db.connect()
    assert conn is not False

def test_execute_sql():
    '''Test a sql select can be performed'''
    db = Database()
    sql = "SELECT 1"
    row = db.execute_select_sql(sql)
    assert row[0] == 1
