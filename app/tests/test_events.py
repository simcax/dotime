'''
    Tests for events
'''
from asyncio import Handle
import pytest
from ..timereg.events import HandleEvents

def test_initialize_event_types():
    '''
        Test of initializing the event types in the database
        These are event types like WorkFromHome or CommutingToWork
    '''
    event_obj = HandleEvents()
    assert event_obj.initialize_events() == True

def test_eventname_can_be_added_when_existing():
    '''
        Test adding an existing event name is possible (It will be ignored 2nd time)
    '''
    event_type_name = "iamunique"
    event_obj = HandleEvents()
    added = event_obj.add_event_type(event_type_name)
    added = event_obj.add_event_type(event_type_name)
    assert added == True

def test_get_event_types():
    '''
        Test we can get the event types from the event handling class
    '''
    event_obj = HandleEvents()
    event_types = event_obj._get_event_types()
    assert len(event_types) > 0

def test_check_of_the_work_from_home_eventtype_exists():
    '''
        Test the work from home event type exists in the database
        This should exist when the app is started, as the app is 
        initializing the event type
    '''
    event_type="WorkFromHome"
    event_obj = HandleEvents()
    event_exists = event_obj.event_type_exists(event_type)
    assert event_exists == True

def test_check_of_the_commute_to_work_eventtype_exists():
    '''
        Test the commute to work event type exists in the database
        This should exist when the app is started, as the app is 
        initializing the event type
    '''
    event_type="CommuteToWork"
    event_obj = HandleEvents()
    event_exists = event_obj.event_type_exists(event_type)
    assert event_exists == True

def test_non_existing_event_type():
    '''
        Test we get false back, when testing for a non-existing event type
    '''
    event_type="idontexist"
    event_obj = HandleEvents()
    event_exists = event_obj.event_type_exists(event_type)
    assert event_exists == False
