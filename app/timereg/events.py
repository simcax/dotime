'''
    Class for handling events
'''
from psycopg2 import DatabaseError
from flask import current_app
from app.db.database import Database

class HandleEvents:
    '''
        This class handles event types for time registration. This could be working from home
        or commuting to work.
    '''
    event_types = ['WorkFromHome','CommuteToWork']


    def initialize_events(self):
        '''
            Method to initialize the database with eventtypes, in case the database is new
            or more likely (in due time at least) new event types are added.
        '''
        event_types = self._get_event_types()
        event_types_initialized = False
        for event in event_types:
            event_types_initialized = self.add_event_type(event)
            if not event_types_initialized:
                break
        return event_types_initialized

    @classmethod
    def add_event_type(cls, event_type):
        '''
            Adds the given event type to the database
            Takes a string with the name of the event type
            Returns True or False as to whether the addition succeeded
        '''
        try:
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                sql = f"INSERT INTO soc.eventtypes (eventname) VALUES ('{event_type}') \
                ON CONFLICT (eventname) \
                DO NOTHING "
                cur.execute(sql)
                conn.commit()
                added = True
        except DatabaseError as error:
            current_app.logger.error("Error executing sql: %s, error: %s",sql, error)
        finally:
            conn.close()
        return added

    def _get_event_types(self):
        '''
            Takes no parameters
            Returns the defined event types
        '''
        return self.event_types

    @classmethod
    def get_event_type(cls,eventname):
        '''
            Retrieves the event with the given eventname
            Takes an eventname (str)
            Returns a dict with the uuid and the eventname
        '''
        try:
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                sql = f"SELECT eventtypeuuid, eventname FROM soc.eventtypes \
                    WHERE eventname = '{eventname}'"
                cur.execute(sql)
                if cur.rowcount:
                    return_is = cur.fetchone()[0]
                else:
                    return_is = False
        except DatabaseError as error:
            current_app.logger.error("Error executing sql: %s, error: %s", sql, error)
        finally:
            conn.close()
        return return_is


    def event_type_exists(self, eventname):
        '''
            Checks for an event type exists and is registered in the database
            Takes the name of the event type and returns True or False
        '''
        event_type_exists = bool( self.get_event_type(eventname) is not False)
        return event_type_exists
