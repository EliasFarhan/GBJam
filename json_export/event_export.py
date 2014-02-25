'''
Created on Feb 19, 2014

@author: efarhan
'''
from json_export.json_export import load_json
from engine.const import log
from engine import level_manager
from engine.sound_manager import SoundEvent, MusicEvent
from levels.dialog_gui import DialogEvent

def load_event(filename, object=None):
    '''
    Load an Event JSON file, then parse it
    '''
    event_data = load_json(filename)
    return parse_event_json(event_data,object=object)
    
def parse_event_json(event_dict,parent_event=None,object=None):
    '''
    Recursively load a file
    
    TODO: do it as a list, not a linked-list and import code from Cavi
    '''
    event_type = ""
    try:
        event_type = event_dict['type']
    except KeyError:
        return None
    except TypeError:
        log("TypeError on event "+str(event_dict),1)
    event = None
    if event_type == 'SoundEvent':
        event = parse_sound_event(event_dict,parent_event,object)
    elif event_type == 'MusicEvent':
        event = parse_music_event(event_dict,parent_event,object)
    elif event_type == 'DialogEvent':
        event = parse_dialog_event(event_dict, parent_event,object)
    
    
    if event and parent_event:
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
    event = DialogEvent(level_manager.get_level(), event_dict["text"])
    answers = {}
    for answer in event_dict['answers'].keys():
        answers[answer] = parse_event_json(event_dict['answers'][answer], event, object)
    event.set_answers(answers)
    try:
        event.next_event = parse_event_json(event_dict["next_event"])
    except KeyError:
        pass
    log(event)
    return event