'''
    Class for handling events
'''
from psycopg2 import DatabaseError, sql
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
                stmt = sql.SQL("""
                    INSERT INTO soc.eventtypes (eventname) VALUES ({event_type})
                    ON CONFLICT (eventname) \
                    DO NOTHING
                """).format(
                    event_type = sql.Literal(event_type)
                )
                cur.execute(stmt)
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
                stmt = sql.SQL("""
                    SELECT eventtypeuuid, eventname FROM soc.eventtypes
                    WHERE eventname = {eventname}
                """).format(
                    eventname = sql.Literal(eventname)
                )
                cur.execute(stmt)
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

    @classmethod
    def is_event_registered(cls, event_type_uuid, the_date, user_id):
        '''
            Checks the events table for a record with the event type uuid, date and users id
            Returns true or false
        '''
        is_registered = False
        try:
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                stmt = sql.SQL("""
                    SELECT 1 FROM soc.events
                    WHERE usersid = {user_id} and eventtypeuuid = {event_type_uuid}
                    and dateofevent = {the_date}
                """).format(
                    user_id = sql.Literal(user_id),
                    event_type_uuid = sql.Literal(event_type_uuid),
                    the_date = sql.Literal(the_date)
                )
                cur.execute(stmt)
                is_registered = bool(cur.rowcount)
        except DatabaseError as error:
            current_app.logger.error("Error executing sql: %s, error: %s", sql, error)
        finally:
            conn.close()
        return is_registered

    @classmethod
    def add_event(cls, event_type_uuid, the_date, user_id):
        '''
            Adds a record in the events table for a given user id, date and event type
            Returns True or False as to whether it was added
        '''
        event_added = False
        try:
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                stmt = sql.SQL("""
                    INSERT INTO soc.events (usersid, eventtypeuuid, dateofevent)
                    VALUES ({user_id},{event_type_uuid},{the_date})
                """).format(
                    user_id = sql.Literal(user_id),
                    event_type_uuid = sql.Literal(event_type_uuid),
                    the_date = sql.Literal(the_date)
                )
                cur.execute(stmt)
                event_added = bool(cur.rowcount)
                conn.commit()
        except DatabaseError as error:
            current_app.logger.error("Error executing sql: %s, error: %s", sql, error)
        finally:
            conn.close()
        return event_added

    @classmethod
    def delete_event(cls, event_type_uuid, the_date, user_id):
        '''
            Deletes a record in the events table for a given user id, date and event type
            Returns True or False as to whether it was added
        '''
        event_deleted = False
        try:
            db_obj = Database()
            conn = db_obj.connect()
            with conn.cursor() as cur:
                stmt = sql.SQL("""
                    DELETE FROM soc.events
                    WHERE usersid = {user_id} and eventtypeuuid = {event_type_uuid}
                    and dateofevent = {the_date}
                """).format(
                    user_id = sql.Literal(user_id),
                    event_type_uuid = sql.Literal(event_type_uuid),
                    the_date = sql.Literal(the_date)
                )
                cur.execute(stmt)
                event_deleted = bool(cur.rowcount)
                current_app.logger.debug("Event deleted status: %s",event_deleted)
                if event_deleted:
                    conn.commit()
        except DatabaseError as error:
            current_app.logger.error("Error executing sql: %s, error: %s", sql, error)
        finally:
            conn.close()
        return event_deleted

    def toggle_event(self, event_type_uuid, the_date, user_id):
        '''
            Adds or removes an event type to the events table
            Takes a user id, an event type uuid and the date of the event
            Returns:
            False = Something went wrong removing or adding the record to the events table
            on = record was added for the user on the given date
            off = record existed with the date for the user in the table and was removed
        '''
        toggled = False
        deleted = False
        added = False
        if self.is_event_registered(event_type_uuid,the_date,user_id):
            current_app.logger.debug("Event is registered. Deleting it.", )
            deleted = self.delete_event(event_type_uuid,the_date,user_id)
        else:
            added = self.add_event(event_type_uuid,the_date,user_id)
        if added:
            toggled = 'on'
        elif deleted:
            toggled = 'off'
        return toggled

    def get_commute_status(self, user_id,the_date):
        '''
            Get's the commute status for the user_id on the given date
            Returns:
                WorkFromHome - if this was registered on the date for the user
                CommuteToWork - if this was registered on the date for the user
                None - neither WorkFromHome nor CommuteToWork was registered yet
                False - More than one is registered
            Only one of the two is able to be registered on a given date
        '''
        event_obj = HandleEvents()
        # Get event types
        work_at_home_event_type = event_obj.get_event_type("WorkFromHome")
        commute_event_type = event_obj.get_event_type("CommuteToWork")
        # Get status for the two
        worked_from_home_status = self.is_event_registered(work_at_home_event_type,the_date,user_id)
        commuted_to_work_status = self.is_event_registered(commute_event_type,the_date,user_id)
        if worked_from_home_status and commuted_to_work_status is False:
            commute_status = "WorkFromHome"
        elif worked_from_home_status is False and commuted_to_work_status:
            commute_status = "CommuteToWork"
        elif worked_from_home_status is False and commuted_to_work_status is False:
            commute_status = None
        else:
            commute_status = False
        return commute_status
