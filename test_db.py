'''Test Database Class'''
from app.db.database import Database

def test_db_initialization():
    db = Database()
    assert db.db_connection_string is not None
