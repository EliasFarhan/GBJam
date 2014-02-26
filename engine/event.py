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

class KEY():
    if not pookoo:
        K_UP = pygame.K_UP
        K_DOWN = pygame.K_DOWN
        K_LEFT = pygame.K_LEFT
        K_RIGHT = pygame.K_RIGHT
        K_ESCAPE = pygame.K_ESCAPE
    else:
        K_UP = 82
        K_DOWN = 81
        K_LEFT = 80
        K_RIGHT = 79
        K_ESCAPE = 41


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

'''button_map = {'action' : 'key'}'''
button_map = {}

'''button_value = {'key' : value}'''
button_value = {}

'''button_key = {'pygame_key': 'key'}'''
button_key = {}

def add_button(action,key_value):
    global button_map,button_value,button_key
    
    button_map[action] = key_value
    button_value[action] = 0
    
    try:
        if (ord('a') <= ord(key_value) <= ord('z')) or \
        (ord('0') <= ord(key_value) <= ord('9')):
            button_key[ord(key_value)] = key_value
    except TypeError:
        '''the key value is not a letter or a number'''
        if key_value == 'UP':
            button_key[KEY.K_UP] = key_value
        if key_value == 'DOWN':
            button_key[KEY.K_DOWN] = key_value
        if key_value == 'LEFT':
            button_key[KEY.K_LEFT] = key_value
        if key_value == 'RIGHT':
            button_key[KEY.K_RIGHT] = key_value
        if key_value == 'ESC':
            button_key[KEY.K_ESCAPE] = key_value
            
            
def get_button(action):
    global button_value,button_map
    try:
        return button_value[button_map[action]]
    except KeyError:
        return False
    
def update_event():
    '''
    Update the states of Input Event
    '''
    global button_key,button_value
    if not pookoo:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                try:
                    button_value[button_key[event.key]] = True
                except KeyError:
                    '''Key not mapped'''
                    pass
                if event.key == pygame.K_TAB:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        from engine.loop import get_console
                        console = get_console()
                        console.set_active()
                        console.preserve_events = False
            elif event.type == pygame.KEYUP:
                try:
                    button_value[button_key[event.key]] = False
                except KeyError:
                    '''Key not mapped'''
                    pass
            elif event.type == pygame.VIDEORESIZE:
                resize_screen(event.w, event.h)
    else:
        for k_value in button_key.keys():
            button_value[button_key[k_value]] = input.keyboard_pressed(k_value)

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


    
