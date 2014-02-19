'''
Created on Feb 19, 2014

@author: efarhan
'''
from engine.event import show_mouse
from engine.init import get_screen_size
from game_object.text import Text

class DialogGUI():
    def __init__(self):
        self.dialog = False
        self.dialog_box = None
        self.dialog_text = Text((0,get_screen_size()[1]*2/3), 
                                get_screen_size()[1]/6, 
                                "comicsansms", "",gradient=60)
        self.dialog_answers = []
    def loop(self,screen):
        '''Dialog'''
        if self.dialog and not self.editor:
            show_mouse()
            for button in self.dialog_answers:
                '''TODO show answers'''
                pass
        
            self.dialog_text.loop(screen, self.screen_pos)