from engine.const import log
from engine.stat import egal_condition, set_value, get_value
from event.event_engine import Event
from json_export.event_json import parse_event_json
from json_export.json_main import get_element

__author__ = 'efarhan'

class ConditionnalEvent(Event):
    def __init__(self,name,value,event1,event2):
        Event.__init__(self)
        self.name = name
        self.value = value
        self.if_event = event1
        self.else_event = event2
    def execute(self):
        if egal_condition(self.name,self.value):
            if self.if_event:
                self.if_event.execute()
        else:
            if self.else_event:
                self.else_event.execute()
    @staticmethod
    def parse_event(event_dict):
        name = get_element(event_dict, "name")
        value = get_element(event_dict,"value")
        if not (name and value):
            log("Invalid arg name and value for ConditionnalEvent",1)
            return None
        if_event = None
        if_event_dict = get_element(event_dict, "if_event")
        if if_event_dict:
            if_event = parse_event_json(if_event_dict)
        else_event = None
        else_event_dict = get_element(event_dict, "else_event")
        if else_event_dict:
            else_event = parse_event_json(else_event_dict)
        return ConditionnalEvent(name, value, if_event, else_event)


class IncreaseValueEvent(Event):
    def __init__(self,name):
        Event.__init__(self)
        self.name = name
    def execute(self):
        set_value(self.name, get_value(sself.name)+1)
        Event.execute(self)
    @staticmethod
    def parse_event(event_dict):
        value_name = get_element(event_dict, "name")
        if value_name:
            return IncreaseValueEvent(value_name)
        else:
            log("Invalid arg for IncreaseValueEvent",1)
            return None


class SetValueEvent(Event):
    def __init__(self,name,value):
        Event.__init__(self)
        self.name = name
        self.value = value
    def execute(self):
        set_value(self.name, self.value)
        Event.execute(self)
    @staticmethod
    def parse_event(event_dict):
        value_name = get_element(event_dict, "name")
        new_value = get_element(event_dict, "value")
        if value_name and new_value:
            return SetValueEvent(value_name,new_value)
        else:
            log("Invalid arg for IncreaseValueEvent",1)
            return None