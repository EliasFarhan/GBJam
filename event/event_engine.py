'''
Created on 17 mars 2014

@author: efarhan
'''
from engine.stat import egal_condition, set_value, get_value
from json_export.json_main import get_element
from engine.const import log
from json_export.event_json import parse_event_json
from engine.level_manager import get_level

class Event():
    def __init__(self):
        self.parent_event = None # for dialog only
        self.next_event = None
    def set_parent_event(self,parent_event):
        self.parent_event = parent_event
        if self.next_event == None:
            self.next_event = parent_event.next_event
    def execute(self):
        if self.next_event:
            self.next_event.execute()
        #for dialog tree only
        elif self.parent_event:
            if self.parent_event.next_event:
                self.parent_event.next_event.execute()
    @staticmethod
    def parse_event(event_dict):
        return Event()









'''
def parse_change_image_event(event_dict,parent_event=None,object=None):
    event = ChangeImageEvent(get_level(), event_dict["name"], event_dict["path"])
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
    
def parse_visual_event(event_dict,parent_event=Nonew_level_name ne,object=None):
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
    return event'''