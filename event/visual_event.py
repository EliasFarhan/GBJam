'''
Created on Feb 26, 2014

@author: efarhan
'''
from event.event_main import Event

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

class ChangeImageEvent(VisualEvent):
    def __init__(self,gamestate,name,path):
        VisualEvent.__init__(self, gamestate, name)
        self.path = path
    def execute(self):
        self.gamestate.characters[self.name].reload(self.path)
        VisualEvent.execute(self)