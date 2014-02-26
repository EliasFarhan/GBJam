'''
Created on Feb 19, 2014

@author: efarhan
'''
from json_export.json_export import load_json
from engine.const import log
from engine.level_manager import get_level
from engine.event import KEY, SoundEvent, MusicEvent, ConditionnalEvent,\
    IncreaseValueEvent, SetValueEvent, DialogEvent, VisualEvent


def load_event(filename, object=None):
    event_data = load_json(filename)
    return parse_event_json(event_data,object=object)
    
def parse_event_json(event_dict,parent_event=None,object=None):
    event_type = ""
    event = None
    try:
        event_type = event_dict['type']
    except KeyError:
        try:
            event = load_event(event_dict['event'], object)
        except KeyError:
            #log("KeyError on event "+str(event_dict),1)
            return None
    except TypeError:
        log("TypeError on event "+str(event_dict),1)
    
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

    if event and parent_event:
        pass#wevent.set_parent_event(parent_event)
    
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