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
from event.keyboard_event import update_keyboard_event
if not pookoo:
    import pygame
else:
    import input
    
def update_event():
    '''
    Update the states of Input Event
    '''
    global button_key,button_value
    if not pookoo:
        for event in pygame.event.get():
            update_keyboard_event(event)
            
            if event.type == pygame.VIDEORESIZE:
                resize_screen(event.w, event.h)
            elif event.type == pygame.QUIT:
                quit()
    else:
        for k_value in button_key.keys():
            button_value[button_key[k_value]] = input.keyboard_pressed(k_value)
    

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



class SwitchEvent(Event):
    def __init__(self,gamestate,new_level_name):
        Event.__init__(self)
        self.gamestate = gamestate
        self.filename = new_level_name
    def execute(self):
        self.gamestate.reload(self.filename)
        Event.execute(self)








    
