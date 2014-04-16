"""
Created on 17 mars 2014

@author: efarhan
"""
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
        if self.next_event is None:
            self.next_event = parent_event.next_event

    def execute(self):
        if self.next_event:
            self.next_event.execute()
        #for dialog tree only
        elif self.parent_event:
            Event.execute(self.parent_event)

    @staticmethod
    def parse_event(event_dict):
        return Event()
