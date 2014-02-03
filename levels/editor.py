'''
Created on Feb 1, 2014

@author: efarhan
'''
from engine.event import get_mouse

class Editor():
    def __init__(self):
        self.editor = False
        self.mouse_clicked = (0,0,0)
        self.current_selected = None
    def loop(self):
        mouse_pos, pressed = get_mouse()
        if pressed[0] and not self.clicked[0]:
            '''Set current_selected'''
            for layer in self.images:
                for image in layer:
                    if image.check_click(mouse_pos,self.screen_pos):
                        self.current_selected = image
            for physic_object in self.physic_objects:
                if physic_object.check_click():
                    self.current_selected = physic_object
            self.clicked = (1, self.clicked[1],self.clicked[2])
            
        if pressed[2]:
            self.current_selected = None
        
        if not pressed[0] and self.clicked[0]:
            self.clicked = (0, self.clicked[1],self.clicked[2])