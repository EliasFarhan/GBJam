'''
TODO: event type can be string for a newfile or a list with events

Created on Feb 19, 2014

@author: efarhan
'''

from json_export.json_main import load_json, get_element
from engine.const import log
from engine.level_manager import get_level



def load_event(filename, object=None):
    event_data = load_json(filename)
    log("Loading event: "+filename)
    return parse_event_json(event_data,object=object)

def parse_event_json(event_dict, parent_event=None, object=None):
    first_event = None
    previous_event = None
    event = None
    try:
        event_data = event_dict['event']
        if event_data.__class__ == list:
            for e in event_data:
                event = parse_event_json(e, parent_event)
                if not first_event:
                    first_event = event
                if previous_event:
                    previous_event.next_event = event
                previous_event = event
            return first_event
        elif event_data.__class__ == str:
            return load_event(event_dict['event'])
    except KeyError:
        return parse_event_type_json(event_dict, parent_event, object)
    except TypeError as e:
        log(str(e)+" "+str(event_dict),1)
        return None

def parse_event_type_json(event_dict,parent_event=None,object=None):
    event = None
    event_type = get_element(event_dict,'type')

    if event_type:
        try:
            from event.event_engine import *
            exec("""event = %s.parse_event(event_dict)"""%(event_type))
        except Exception as e:
            log("Error with event type: "+event_type+" \nException: "+e,1)
            return None
    next_event_dict = get_element(event_dict, "next_event")
    if next_event_dict:
        event.next_event = parse_event_json(next_event_dict)
    return event





def parse_conditionnal_event(event_dict,parent_event=None,object=None):

    if_event = parse_event_json(event_dict["if_event"], parent_event, object)
    else_event = parse_event_json(event_dict["else_event"], parent_event, object)
    event = ConditionnalEvent(event_dict["name"], event_dict["value"], if_event, else_event)

    return event
