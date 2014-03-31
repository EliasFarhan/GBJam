
'''
Manage physics, input event 
and create a root for Event Engine 

Created on 8 sept. 2013

@author: efarhan
'''


from engine.init import resize_screen

from event.keyboard_event import update_keyboard_event
from engine.const import CONST


if CONST.render == 'sfml':
    import sfml

    
def update_event():
    '''
    Update the states of Input Event
    '''
    global button_key,button_value
    if CONST.render == 'sfml':
        from engine.loop import get_screen
        window = get_screen()
        for event in window.events:
            update_keyboard_event(event)
            
            if type(event) is sfml.CloseEvent:
                from engine.loop import set_finish
                set_finish()

