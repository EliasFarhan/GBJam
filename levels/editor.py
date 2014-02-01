'''
Created on Feb 1, 2014

@author: efarhan
'''
from engine.event import get_mouse

class Editor():
    def __init__(self):
        self.editor = False
        self.mouse_clicked = (0,0,0)
    def loop(self):
        mouse_pos, pressed = get_mouse()
        if pressed[0] and not self.clicked[0]:
            '''TODO : Set current_selected'''
            
            self.clicked = (1, self.clicked[1],self.clicked[2])
            
        if pressed[2]:
            self.current_selected = None
        
        if not pressed[0] and self.clicked[0]:
            self.clicked = (0, self.clicked[1],self.clicked[2])