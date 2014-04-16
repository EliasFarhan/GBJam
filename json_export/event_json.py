"""

Created on Feb 19, 2014

@author: efarhan
"""

from json_export.json_main import load_json, get_element
from engine.const import log, CONST


def load_event(filename, parent_event=None, obj=None):
    event_data = load_json(filename)
    log("Loading event: " + filename)
    return parse_event_json(event_data, parent_event=parent_event, obj=obj)


def parse_event_json(event_dict, parent_event=None, obj=None):
    first_event = None
    previous_event = None
    event = None
    try:
        event_data = event_dict['event']
        if isinstance(event_data, list):
            for e in event_data:
                event = parse_event_json(e, parent_event)
                if not first_event:
                    first_event = event
                if previous_event:
                    previous_event.next_event = event
                previous_event = event
            return first_event
        elif isinstance(event_data, CONST.string_type):
            return load_event(event_dict['event'])
    except KeyError:
        return parse_event_type_json(event_dict, parent_event, obj)
    except TypeError as e:
        log(str(e) + " " + str(event_dict), 1)
        return None


def parse_event_type_json(event_dict, parent_event=None, object=None):
    event = None
    event_type = get_element(event_dict, 'type')
    if event_type and isinstance(event_type, CONST.string_type):
        for c in event_type:
            if c != '.' and c != '_' and not c.isalpha():
                log("Error: Invalid character type for event type (only alphanumeric '.' and '_'): " + event_type, 1)
                return None
    elif event_type is None:
        event_type = ''

    if event_type:
        dir_list = event_type.split(".")

        module_name = ".".join(dir_list[0:len(dir_list) - 1])
        class_name = dir_list[len(dir_list) - 1]
        log('Loading: ' + module_name + "." + class_name)
        try:
            exec ('''from %s import %s''' % (module_name, class_name ))
        except ImportError as e:
            log("Error while importing " + event_type + " " + str(e), 1)
            return None

        try:
            d = locals()
            exec ('''event = %s.parse_event(event_dict)''' % class_name, globals(), d)
            event = d['event']
        except Exception as e:
            log("Error initializing event: " + str(e), 1)
            return None
    next_event_dict = get_element(event_dict, "next_event")
    if next_event_dict:
        event.next_event = parse_event_json(next_event_dict)
    return event


