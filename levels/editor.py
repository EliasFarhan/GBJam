'''
Created on Feb 1, 2014

@author: efarhan
'''

from engine.const import log, CONST
from engine.init import get_screen_size
from engine.vector import Vector2
from event.event_main import add_button, get_button
from event.mouse_event import get_mouse, show_mouse
from game_object.game_object_main import GameObject
from game_object.text import Text
from json_export.level_json import save_level


class Editor():
    def __init__(self):

        add_button('editor', 'LCTRL+e')
        self.editor_click = False

        self.editor = False
        self.text_size = 50

        self.mouse_clicked = (0, 0, 0)
        self.current_selected = None


        self.scale_clicked = (0, 0)  #red, enlarg

        self.save_clicked = False

        add_button('scale_y_down', ['DOWN'])
        add_button('scale_y_up', ['UP'])
        add_button('scale_x_down', ['LEFT'])
        add_button('scale_x_up', ['RIGHT'])

        add_button('angle_up',['a'])
        add_button('angle_down',['d'])

        add_button('save', ['LCTRL+s'])

        add_button('box',['LCTRL'])

        self.new_obj = None
        self.new_obj_pos = Vector2()


        self.obj_init_pos = Vector2()
        self.mouse_init_pos = Vector2()

        '''GUI'''
        self.gui_editor_mode = Text(Vector2(0,get_screen_size().y-2*self.text_size), self.text_size, "data/font/pixel_arial.ttf", "Editor mode", relative=True)
        self.gui_current_selected = Text(Vector2(0,get_screen_size().y-self.text_size), self.text_size, "data/font/pixel_arial.ttf", "",relative=True)
        self.gui_saved = Text(Vector2(0,0), self.text_size, "data/font/pixel_arial.ttf", "Saved",relative=True)

    def loop(self, screen,screen_pos):
        if not (self.editor_click or not get_button('editor')):
            self.editor = not self.editor
            self.lock = self.editor
            self.editor_click = True
            if self.editor:
                log("Editor mode activate")
            else:
                self.current_selected = None
        if not get_button('editor'):
            self.editor_click = False
        if self.editor:
            show_mouse()

        mouse_pos, pressed = get_mouse()
        if not self.editor:
            return

        self.gui_editor_mode.loop(screen,screen_pos)

        '''Save Level'''
        if self.save_clicked:
            self.gui_saved.loop(screen,screen_pos)
        if get_button('save') and not self.save_clicked:
            save_level(self)
            self.save_clicked = True
        elif not get_button('save'):
            self.save_clicked = False

        '''Left click,
        select a object and move it'''
        if not get_button('box'):
            self.new_obj = None
            if pressed[0] and not self.mouse_clicked[0]:
                '''Set current_selected'''
                self.current_selected = None
                for layer in self.objects:
                    for image in layer:
                        if image.check_click(mouse_pos, self.screen_pos):
                            log("Current_object is: " + str(image))
                            self.current_selected = image
                            self.obj_init_pos = self.current_selected.pos
                            self.mouse_init_pos = mouse_pos + self.screen_pos
                self.mouse_clicked = (1, self.mouse_clicked[1], self.mouse_clicked[2])
            elif pressed[0] and self.mouse_clicked[0]:
                '''Move the current object'''
                if self.current_selected is not None:
                    self.current_selected.set_pos(self.obj_init_pos, mouse_pos + self.screen_pos - self.mouse_init_pos)
        else:
            if pressed[0] and not self.mouse_clicked[0]:
                self.mouse_clicked = (1, self.mouse_clicked[1], self.mouse_clicked[2])
                self.new_obj = GameObject()
                self.new_obj.pos = mouse_pos + self.screen_pos
                self.objects[4].append(self.new_obj)
            elif self.mouse_clicked[0]:
                self.new_obj.size = mouse_pos + self.screen_pos - self.new_obj.pos
                self.new_obj.update_rect()

        if not pressed[0] and self.mouse_clicked[0]:
            self.mouse_clicked = (0, self.mouse_clicked[1], self.mouse_clicked[2])

        if self.current_selected:
            self.gui_current_selected.change_text(str(self.current_selected.__class__)+" "+str(self.current_selected.id))
            self.gui_current_selected.loop(screen, screen_pos)

        '''Size scale'''
        scale_x = get_button("scale_x_up")-get_button("scale_x_down")
        scale_y = get_button("scale_y_up")-get_button("scale_y_down")

        if self.current_selected:
            self.current_selected.scale(scale_x,scale_y)
        '''Angle'''
        angle = get_button("angle_up")-get_button("angle_down")
        if self.current_selected:
            self.current_selected.rotate(angle)