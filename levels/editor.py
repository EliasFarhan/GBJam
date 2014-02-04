'''
Created on Feb 1, 2014

@author: efarhan
'''
from engine.event import get_mouse, add_button, get_button
from engine.const import log

class Editor():
    def __init__(self):
        self.editor = False
        self.mouse_clicked = (0,0,0)
        self.current_selected = None
        
        add_button('move_right','a')
        add_button('move_left', 'd')
        add_button('move_up', 'w')
        add_button('move_down', 's')
        
        add_button('scale_red', 'DOWN')
        add_button('scale_enlarg', 'UP')
        add_button('rotate_left', 'LEFT')
        add_button('rotate_right', 'RIGHT')
    def loop(self):
        
        mouse_pos, pressed = get_mouse()
        if pressed[0] and not self.mouse_clicked[0]:
            log("Click")
            '''Set current_selected'''
            for layer in self.images:
                for image in layer:
                    if image.check_click(mouse_pos,self.screen_pos):
                        log("Image clicked")
                        self.current_selected = image
                        
            for physic_object in self.physic_objects:
                if physic_object.check_click(mouse_pos,self.screen_pos):
                    log("Physic_object clicked")
                    self.current_selected = physic_object
            self.mouse_clicked = (1, self.mouse_clicked[1],self.mouse_clicked[2])
            
        if pressed[2]:
            self.current_selected = None
        
        if not pressed[0] and self.mouse_clicked[0]:
            log("Unclick")
            self.mouse_clicked = (0, self.mouse_clicked[1],self.mouse_clicked[2])
            
        '''Keyboard event'''
        if get_button('move_right'):
            pass
        if get_button('move_left'):
            pass
        if get_button('move_up'):
            pass
        if get_button('move_down'):
            pass
        
        if get_button('scale_red'):
            pass
        if get_button('scale_enlarg'):
            pass
        if get_button('rotate_left'):
            pass
        if get_button('rotate_right'):
            pass