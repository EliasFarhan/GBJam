'''
Created on Feb 19, 2014

@author: efarhan
'''
from json_export.json_export import load_json
from engine.event import SoundEvent, MusicEvent, DialogEvent
from engine.const import log
from engine import level_manager

def load_event(filename, object=None):
    event_data = load_json(filename)
    return parse_event_json(event_data,object=object)
    
def parse_event_json(event_dict,parent_event=None,object=None):
    event_type = event_dict['type']
    event = None
    if event_type == 'SoundEvent':
        event = parse_sound_event(event_dict,parent_event,object)
    elif event_type == 'MusicEvent':
        event = parse_music_event(event_dict,parent_event,object)
    elif event_type == 'DialogEvent':
        event = parse_dialog_event(event_dict, parent_event,object)
    if parent_event != None:
        event.set_parent_event(parent_event)
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
    log(event)
    return event
def parse_dialog_event(event_dict,parent_event=None,object=None):
    event = DialogEvent(level_manager.get_level(), event_dict["txt"])
    answers = {}
    for item in event_dict['answers']:
        answers[item[0]] = parse_event_json(item[1], event, object)
    event.set_answers(answers)
    try:
        event.next_event = parse_event_json(event_dict["next_event"])
    except KeyError:
        pass
    log(event)
    return event