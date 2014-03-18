
'''
Manage physics, input event 
and create a root for Event Engine 

Created on 8 sept. 2013

@author: efarhan
'''


from engine.init import resize_screen
from engine.sound_manager import load_sound, play_sound, set_playlist
from engine.stat import egal_condition, set_value, get_value
from event.keyboard_event import update_keyboard_event
from engine.const import render


if render == 'pygame':
    import pygame
elif render == 'sfml':
    import sfml

    
def update_event():
    '''
    Update the states of Input Event
    '''
    global button_key,button_value
    if render == 'pygame':
        for event in pygame.event.get():
            update_keyboard_event(event)
            
            if event.type == pygame.VIDEORESIZE:
                resize_screen(event.w, event.h)
            elif event.type == pygame.QUIT:
                from engine.loop import set_finish
                set_finish()
    elif render == 'sfml':
        from engine.loop import get_screen
        window = get_screen()
        for event in window.events:
            update_keyboard_event(event)
            
            if type(event) is sfml.CloseEvent:
                from engine.loop import set_finish
                set_finish()

class Event():
    '''Abstract class of Event'''
    def __init__(self):
        self.parent_event = None # for dialog only
        self.next_event = None
    def set_parent_event(self,parent_event):
        '''Used for DialogEvent'''
        self.parent_event = parent_event
        if self.next_event == None:
            self.next_event = parent_event.next_event
    def execute(self):
        if self.next_event:
            self.next_event.execute()
        elif self.parent_event:
            '''for DialogEvent tree'''
            if self.parent_event.next_event:
                self.parent_event.next_event.execute()
    @staticmethod
    def parse_event():
        '''Must be implemented by any children'''
        pass

            






class SwitchEvent(Event):
    def __init__(self,gamestate,new_level_name):
        Event.__init__(self)
        self.gamestate = gamestate
        self.filename = new_level_name
    def execute(self):
        self.gamestate.reload(self.filename)
        Event.execute(self)








    
=======
'''
Manage physics, input event 
and create a root for Event Engine 

Created on 8 sept. 2013

@author: efarhan
'''


from engine.init import resize_screen
from engine.sound_manager import load_sound, play_sound, set_playlist
from engine.stat import egal_condition, set_value, get_value
from event.keyboard_event import update_keyboard_event
from engine.const import render


if render == 'pygame':
    import pygame
elif render == 'sfml':
    import sfml

    
def update_event():
    '''
    Update the states of Input Event
    '''
    global button_key,button_value
    if render == 'pygame':
        for event in pygame.event.get():
            update_keyboard_event(event)
            
            if event.type == pygame.VIDEORESIZE:
                resize_screen(event.w, event.h)
            elif event.type == pygame.QUIT:
                from engine.loop import set_finish
                set_finish()
    elif render == 'sfml':
        from engine.loop import get_screen
        window = get_screen()
        for event in window.events:
            update_keyboard_event(event)
            
            if type(event) is sfml.CloseEvent:
                from engine.loop import set_finish
                set_finish()







    
>>>>>>> c3a3ceb14afc29832f3020127a3d062961e58217
