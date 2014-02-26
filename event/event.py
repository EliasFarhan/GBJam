'''
Manage physics, input event 
and create a root for Event Engine 

Created on 8 sept. 2013

@author: efarhan
'''

from engine.const import pookoo, log
from engine.init import resize_screen
from engine.sound_manager import load_sound, play_sound, set_playlist
from engine.stat import egal_condition, set_value, get_value
if not pookoo:
    import pygame
else:
    import input
    
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

class SoundEvent(Event):
    def __init__(self,sound_name):
        Event.__init__(self)
        self.sound_name = sound_name
        self.sound = load_sound(sound_name)
    def execute(self):
        play_sound(self.sound)
        Event.execute(self)

class MusicEvent(Event):
    def __init__(self,playlist):
        Event.__init__(self)
        self.playlist = playlist
    def execute(self):
        set_playlist(self.playlist)
        Event.execute(self)

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


class DialogEvent(Event):
    def __init__(self,gamestate,text,text2=""):
        Event.__init__(self)
        self.text = text
        self.text2 = text2
        self.answers = {}
        self.gamestate = gamestate
    def set_answers(self,answers):
        self.answers = answers
    def execute(self):
        self.gamestate.dialog = True
        self.gamestate.dialog_text.set_text(self.text)
        self.gamestate.dialog_text2.set_text(self.text2)

        self.gamestate.set_answers(self.answers.keys())
        self.gamestate.dialog_event = self
    def answer(self,answer=None):
        self.gamestate.dialog = False
        new_event = None
        if answer:
            new_event = self.answers[answer]
        
        if new_event:
            new_event.execute()
        else:
            Event.execute(self)

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

class SwitchEvent(Event):
    def __init__(self,gamestate,new_level_name):
        Event.__init__(self)
        self.gamestate = gamestate
        self.filename = new_level_name
    def execute(self):
        self.gamestate.reload(self.filename)
        Event.execute(self)




physics_events = []

def add_physics_event(event):
    global physics_events
    physics_events.append(event)
def get_physics_event():
    global physics_events
    result = []
    for i in range(len(physics_events)):
        result.append(physics_events.pop())
    return result


class PhysicsEvent:
    def __init__(self,a,b,begin):
        self.a=a
        self.b=b
        self.begin=begin


def get_mouse():
    '''
    Return mouse state as 
    position, (left, middle, right)
    '''
    return pygame.mouse.get_pos(), pygame.mouse.get_pressed()

def show_mouse(show=True):
    '''
    Show mouse on display
    '''
    if not pookoo:
        pygame.mouse.set_visible(show)



    
