'''
TODO: event type can be string for a newfile or a list with events

Created on Feb 19, 2014

@author: efarhan
'''

from json_export.json_main import load_json
from engine.const import log
from engine.level_manager import get_level
from event.visual_event import VisualEvent, ChangeImageEvent
from event.event_main import SetValueEvent, SwitchEvent, IncreaseValueEvent,\
    ConditionnalEvent, DialogEvent
from event.sound_event import SoundEvent, MusicEvent


def load_event(filename, object=None):
    event_data = load_json(filename)
    return parse_event_json(event_data,object=object)

def parse_event_json(event_dict, parent_event=None, object=None):
    first_event = None
    previous_event = None
    event = None
    try:
        event_data = event_dict['event']
        if event_data.__class__ == builtins.list:
            for e in event_data['event']:
                event = parse_event_json(e, parent_event, object)
                if not first_event:
                    first_event = event
                if previous_event:
                    previous_event.next_event = event
                previous_event = event
            return first_event
        elif event_data.__class__ == builtins.str:
            return load_event(event_dict['event'], object)
    except KeyError:
        return parse_event_type_json(event_dict, parent_event, object)
def parse_event_type_json(event_dict,parent_event=None,object=None):
    event = None
    event_type = ''
    try:
        event_type = event_dict['type']
    except KeyError:
        return None
        
    
    if event_type == 'SoundEvent':
        event = parse_sound_event(event_dict,parent_event,object)
    elif event_type == 'MusicEvent':
        event = parse_music_event(event_dict,parent_event,object)
    elif event_type == 'DialogEvent':
        event = parse_dialog_event(event_dict, parent_event,object)
    elif event_type == 'VisualEvent':
        event = parse_visual_event(event_dict, parent_event, object)
    elif event_type == 'ConditionnalEvent':
        event = parse_conditionnal_event(event_dict, parent_event, object)
    elif event_type == 'IncreaseValueEvent':
        event = parse_increase_value(event_dict, parent_event, object)
    elif event_type == 'SwitchLevelEvent':
        log(str(event_dict))
        event = parse_switch_level_event(event_dict, parent_event, object) 
    elif event_type == 'SetValueEvent':
        event = parse_set_value_event(event_dict, parent_event, object)

    
    return event

def parse_visual_event(event_dict,parent_event=None,object=None):
    pos = None
    try:
        pos = event_dict["pos"]
    except KeyError:
        pass
    next_pos = None
    try:
        next_pos = event_dict["next_pos"]
    except KeyError:
        pass
    size = 1
    try:
        size = event_dict["size"]
    except KeyError:
        pass
    name = ""
    try:
        name = event_dict["name"]
    except KeyError:
        pass
    names = []
    try:
        names = event_dict["names"]
    except KeyError:
        pass
    event = VisualEvent(get_level(), name, names, pos, next_pos, size)
    try:
        event.next_event = parse_event_json(event_dict["next_event"])
    except KeyError:
        pass
    return event

def parse_default_event(event_dict,parent_event=None,object=None):
    '''
    TODO: automatic Event loading with exec
    '''
    pass
    
def parse_set_value_event(event_dict,parent_event=None,object=None):
    event = SetValueEvent(event_dict["name"], event_dict["value"])
    try:
        event.next_event = parse_event_json(event_dict["next_event"])
    except KeyError:
        pass
    return event

def parse_switch_level_event(event_dict,parent_event=None,object=None):
    event = SwitchEvent(get_level(), event_dict["name"])
    try:
        event.next_event = parse_event_json(event_dict["next_event"])
    except KeyError:
        pass
    return event
def parse_increase_value(event_dict,parent_event=None,object=None):
    event = IncreaseValueEvent(event_dict["name"])
    try:
        event.next_event = parse_event_json(event_dict["next_event"])
    except KeyError:
        pass
    return event
def parse_conditionnal_event(event_dict,parent_event=None,object=None):

    if_event = parse_event_json(event_dict["if_event"], parent_event, object)
    else_event = parse_event_json(event_dict["else_event"], parent_event, object)
    event = ConditionnalEvent(event_dict["name"], event_dict["value"], if_event, else_event)

    return event
def parse_change_image_event(event_dict,parent_event=None,object=None):
    event = ChangeImageEvent(get_level(), event_dict["name"], event_dict["path"])
    try:
        event.next_event = parse_event_json(event_dict["next_event"])
    except KeyError:
        pass
    return event

def parse_sound_event(event_dict,parent_event=None,object=None):
    event = SoundEvent(event_dict["path"])
    try:
        event.next_event = parse_event_json(event_dict["next_event"])
    except KeyError:
        pass
    return event

def parse_music_event(event_dict,parent_event=None,object=None):
    event = MusicEvent(event_dict["playlist"])
    try:
        event.next_event = parse_event_json(event_dict["next_event"])
    except KeyError:
        pass

    return event

def parse_dialog_event(event_dict,parent_event=None,object=None):
    text2 = ""
    try:
        text2 = event_dict["text2"]
    except KeyError:
        pass
    event = DialogEvent(get_level(), event_dict["text"],text2)
    try:
        event.next_event = parse_event_json(event_dict["next_event"])
        if not event.next_event:
            if parent_event:
                event.next_event = parent_event.next_event
    except KeyError:
        pass
    try:
        answers = {}
        for answer in event_dict['answers'].keys():
            answers[answer] = parse_event_json(event_dict['answers'][answer], event, object)
        event.set_answers(answers)
    except KeyError:
        pass
    return event