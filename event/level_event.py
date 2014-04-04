from engine.const import log
from engine.level_manager import get_level
from event.event_engine import Event
from json_export.json_main import get_element

__author__ = 'efarhan'

class VisualEvent(Event):
    def __init__(self,gamestate,name="",names=[],pos=None,next_pos=None,size=1):
        self.gamestate = gamestate
        self.name = name
        self.names = names


        self.pos = pos
        self.next_pos = next_pos
        self.size = size
        Event.__init__(self)

    def change(self,names=[]):
        for name in names:

            self.gamestate.characters[name].index = self.size
            if self.pos:
                self.gamestate.characters[name].pos = self.pos
            if self.next_pos:
                self.gamestate.characters[name].next_pos = self.next_pos
            self.gamestate.characters[name].update_rect()

    def execute(self):
        if self.name != "":
            self.change([self.name])
        elif self.names != []:
            self.change(self.names)
        Event.execute(self)

    @staticmethod
    def parse_event(event_dict):
        return Event.parse_event(event_dict)


class SwitchEvent(Event):
    def __init__(self,gamestate,new_level_name):
        Event.__init__(self)
        self.gamestate = gamestate
        self.filename = new_level_name
    def execute(self):
        self.gamestate.reload(self.filename)
        Event.execute(self)
    @staticmethod
    def parse_event(event_dict):
        new_level_name = get_element(event_dict,"name")
        if new_level_name:
            return SwitchEvent(get_level(),new_level_name)
        else:
            log("Invalid arg name for SwitchEvent")

