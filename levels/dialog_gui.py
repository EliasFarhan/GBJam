'''
Created on Feb 19, 2014

@author: efarhan
'''
from engine.event import show_mouse
from engine.init import get_screen_size
from game_object.text import Text
from game_object.image import Image
from engine.image_manager import load_image, show_image

class DialogGUI():
    def __init__(self):
        self.dialog = False
        self.dialog_box = load_image("data/sprites/gui/dialog_box.png")
        self.dialog_text = Text((50,get_screen_size()[1]*2/3+10), 
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
            show_image(self.dialog_box, screen, 
                       (0,get_screen_size()[1]*2/3), 
                       new_size=(get_screen_size()[0],int(get_screen_size()[1]/3)))
            self.dialog_text.loop(screen, self.screen_pos)