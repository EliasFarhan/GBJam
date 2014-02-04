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
        self.scale_clicked = (0,0)#red, enlarg
        
        add_button('move_right','d')
        add_button('move_left', 'a')
        add_button('move_up', 'w')
        add_button('move_down', 's')
        
        add_button('scale_red', 'DOWN')
        add_button('scale_enlarg', 'UP')
        add_button('rotate_left', 'LEFT')
        add_button('rotate_right', 'RIGHT')
    def loop(self):
        
        mouse_pos, pressed = get_mouse()
        
        if pressed[0] and not self.mouse_clicked[0]:
            '''Set current_selected'''
            for layer in self.images:
                for image in layer:
                    if image.check_click(mouse_pos,self.screen_pos):
                        self.current_selected = image
                        
            for physic_object in self.physic_objects:
                if physic_object.check_click(mouse_pos,self.screen_pos):
                    self.current_selected = physic_object
            self.mouse_clicked = (1, self.mouse_clicked[1],self.mouse_clicked[2])
            
        if pressed[2]:
            self.current_selected = None
        
        if not pressed[0] and self.mouse_clicked[0]:
            self.mouse_clicked = (0, self.mouse_clicked[1],self.mouse_clicked[2])
            
        '''Keyboard event'''
        if self.current_selected != None:
            if get_button('move_right'):
                self.current_selected.move(horizontal=1)
            if get_button('move_left'):
                self.current_selected.move(horizontal=-1)
            if get_button('move_up'):
                self.current_selected.move(vertical=-1)
            if get_button('move_down'):
                self.current_selected.move(vertical=1)
            
            if not self.scale_clicked[0] and get_button('scale_red'):
                self.current_selected.scale(False)
                self.scale_clicked = (1,self.scale_clicked[1])
            else:
                self.scale_clicked = (0,self.scale_clicked[1])
            
            if not self.scale_clicked[1] and get_button('scale_enlarg'):
                self.current_selected.scale(True)
                self.scale_clicked = (self.scale_clicked[0],1)
            else:
                self.scale_clicked = (self.scale_clicked[1],0)
            
            if get_button('rotate_left'):
                self.current_selected.rotate(False)
            if get_button('rotate_right'):
                self.current_selected.rotate(True)