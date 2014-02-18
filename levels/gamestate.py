'''
Created on 9 dec. 2013

@author: efarhan
'''

from engine.scene import Scene
from engine.const import log, debug
from levels.level_export import load_level, save_level
from engine.physics import init_physics, update_physics,deinit_physics
from levels.editor import Editor
from engine.event import show_mouse, add_button, get_button


class GameState(Scene,Editor):
    def __init__(self,filename):
        self.filename = filename
        if debug:
            Editor.__init__(self)
    def __del__(self):
        deinit_physics()
    def init(self):
        init_physics()
        self.images = [
                       [],
                       [],
                       [],
                       [],
                       [],]
        self.physic_objects = [
                                ]
        self.screen_pos = (0,0)
        if self.filename != "":
            log("Loading level "+self.filename)
            if not load_level(self):
                from engine.level_manager import switch_level
                switch_level(Scene())
        
        add_button('editor', 'e')
        self.editor_click = False
        
        '''current dialog'''
        self.dialog = False
        self.dialog_box = None
        self.dialog_text = ''
        self.dialog_answers = []
        
        
        
    def reload(self,newfilename):
        self.filename = newfilename
        self.init()
    def loop(self, screen):
        '''Dialog'''
        if self.dialog and not self.editor:
            show_mouse()
            for button in self.dialog_answers:
                '''show answers'''
                pass
        
        '''Event
        TODO: if mouse_click on element, execute its event, of not null'''
        
        
        '''Editor'''
        
        if not self.editor_click and get_button('editor'):
            self.editor = not self.editor
            if not self.editor:
                save_level(self)
            self.editor_click = True
        if not get_button('editor'):
            self.editor_click = False
        if debug and self.editor:
            show_mouse()
            Editor.loop(self)
        
        if not self.editor:
            update_physics()
            
        '''Show images'''
        for i in range(self.player.layer):
            for j in range(len(self.images[i])):
                self.images[i][j].loop(screen,self.screen_pos)
        self.screen_pos = self.player.loop(screen,self.screen_pos,self.editor)
        for i in range(self.player.layer,len(self.images)):
            for j in range(len(self.images[i])):
                self.images[i][j].loop(screen,self.screen_pos)
        for physic_object in self.physic_objects:
            physic_object.loop(screen,self.screen_pos)
    def exit(self, screen):
        deinit_physics()
        Scene.exit(self, screen)
