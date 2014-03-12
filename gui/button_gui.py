'''
Created on Feb 26, 2014

@author: efarhan
'''
from game_object.game_object_main import GameObject
from game_object.text import Text
from game_object.image import Image

class ButtonGUI(GameObject):
    def __init__(self,pos,size,button_img='',button_text='',font='',show=False,margin=10):
        GameObject.__init__(self)
        self.pos = pos
        self.size = size
        self.update_rect(self)
        self.button_image = None
        if button_img != '':
            self.button_image = Image(button_img, pos, size=size)
        self.text = Text(pos, size, font, text=button_text)
    def set_text(self,text):
        self.text.change_text(text)
    def loop(self,screen,screen_pos):
        if self.show:
            if self.button_image:
                self.button_image.loop(screen,screen_pos)
            if self.button_text:
                self.button_text.loop(screen,screen_pos)
    
    def execute_event(self):
        GameObject.execute_event(self)

class DialogGUI(GameObject):
    pass