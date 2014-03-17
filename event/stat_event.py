'''
Created on Mar 17, 2014

@author: efarhan
'''
from event.event_main import Event
from engine.stat import set_value, get_value, egal_condition
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
            
class IncreaseValueEvent(Event):
    def __init__(self,name):
        Event.__init__(self)
        self.name = name
    def execute(self):
        set_value(self.name, get_value(self.name)+1)
        Event.execute(self)
class SetValueEvent(Event):
    def __init__(self,name,value):
        Event.__init__(self)
        self.name = name
        self.value = value
    def execute(self):
        set_value(self.name, self.value)
        Event.execute(self)