'''
Created on Feb 19, 2014

@author: efarhan
'''
from engine.event import show_mouse, Event
from engine.init import get_screen_size
from game_object.text import Text
from game_object.image import Image
from engine.image_manager import load_image, show_image

class DialogEvent(Event):
    def __init__(self,gamestate,text):
        Event.__init__(self)
        self.text = text
        self.answers = {}
        self.gamestate = gamestate
    def set_answers(self,answers):
        self.answers = answers
    def execute(self):
        self.gamestate.dialog = True
        self.gamestate.dialog_text.set_text(self.text)
        self.gamestate.set_answers(self.answers.keys())
    def answer(self,answer):
        self.gamestate.dialog = False
        new_event = self.answers[answer]
        if new_event:
            new_event.execute()
        else:
            Event.execute(self)

class DialogGUI():
    def __init__(self):
        self.dialog = False
        self.dialog_box = load_image("data/sprites/gui/dialog_box.png")
        self.dialog_text = Text((50,get_screen_size()[1]*2/3+10), 
                                get_screen_size()[1]/7, 
                                "comicsansms", "",gradient=60)
        self.dialog_answers = []
    def set_answers(self,answers):
        for item in answers:
            pass
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