'''
Created on Feb 1, 2014

@author: efarhan
'''

from engine.const import log, CONST
from engine.vector import Vector2
from event.event_main import add_button, get_button
from event.mouse_event import get_mouse, show_mouse
from json_export.level_json import save_level


class Editor():
    def __init__(self):
        
        add_button('editor', 'e')
        self.editor_click = False
        
        self.editor = False
        self.mouse_clicked = (0,0,0)
        self.current_selected = None
        self.scale_clicked = (0,0)#red, enlarg

        self.save_clicked = False
        
        add_button('scale_red', ['DOWN'])
        add_button('scale_enlarg', ['UP'])
        add_button('rotate_left', ['LEFT'])
        add_button('rotate_right', ['RIGHT'])

        add_button('save',['LCTRL+s'])

        self.obj_init_pos = Vector2()
        self.mouse_init_pos = Vector2()
    
    def loop(self):
        if not self.editor_click and get_button('editor'):
            self.editor = not self.editor
            self.lock = self.editor
            self.editor_click = True
            if self.editor:
                log("Editor mode activate")
        if not get_button('editor'):
            self.editor_click = False
        if self.editor:
            show_mouse()

        mouse_pos, pressed = get_mouse()
        if not self.editor:
            return

        '''Save Level'''
        if get_button('save') and not self.save_clicked:
            save_level(self)
            self.save_clicked = True
        elif not get_button('save'):
            self.save_clicked = False


        '''Left click,
        select a object and move it'''
        if pressed[0] and not self.mouse_clicked[0]:
            '''Set current_selected'''
            for layer in self.images:
                for image in layer:
                    if image.check_click(mouse_pos, self.screen_pos):
                        log("Current_object is: "+str(image))
                        self.current_selected = image
                        self.obj_init_pos = self.current_selected.pos
                        self.mouse_init_pos = mouse_pos+self.screen_pos
            self.mouse_clicked = (1, self.mouse_clicked[1],self.mouse_clicked[2])
        elif pressed[0] and self.mouse_clicked[0]:
            '''Move the current object'''
            if self.current_selected is not None:
                self.current_selected.set_pos(self.obj_init_pos,mouse_pos+self.screen_pos-self.mouse_init_pos)
        if pressed[1]:
            self.current_selected = None

        if not pressed[0] and self.mouse_clicked[0]:
            self.mouse_clicked = (0, self.mouse_clicked[1],self.mouse_clicked[2])

        '''Keyboard event
        if self.current_selected is not None:
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
                self.current_selected.rotate(-1)
            if get_button('rotate_right'):
                self.current_selected.rotate(1)
                        '''