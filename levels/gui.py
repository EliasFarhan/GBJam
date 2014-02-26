'''
Created on Feb 26, 2014

@author: efarhan
'''
from engine.event import show_mouse, Event, get_mouse
from engine.init import get_screen_size
from game_object.text import Text
from game_object.image import Image
from engine.image_manager import load_image, show_image


class GUI():
    def __init__(self):
        self.dialog = False
        self.dialog_box = Image("data/sprites/gui/dialog_box.png", 
                                pos=(0,get_screen_size()[1]*2/3), 
                                size=(get_screen_size()[0],int(get_screen_size()[1]/3)))
        self.dialog_text = Text((50,get_screen_size()[1]*2/3+10), 
                                get_screen_size()[1]/7, 
                                "comicsansms", "",gradient=60)
        self.dialog_text2 = Text((50,get_screen_size()[1]*5/6), 
                                get_screen_size()[1]/7, 
                                "comicsansms", "",gradient=60)
        self.answer_text = []
        self.dialog_answers = []
        self.dialog_event = None
        
        self.show_mouse = True
    def set_answers(self,answers):
        
        del self.answer_text[:]
        del self.dialog_answers[:]
        i = 0
        answer_nmb = len(answers)
        for answer in answers:
            pos = (int(3/4*get_screen_size()[0]),int((2/3-(answer_nmb-i)*1/6)*get_screen_size()[1]))
            size = (int(1/4*get_screen_size()[0]),int(1/6*get_screen_size()[1]))
            self.answer_text.append(Text(pos, size, "comicsansms", answer))
            self.dialog_answers.append(Image("data/sprites/gui/dialog_box.png", pos, size=size))
            i+=1
    def loop(self,screen):
        '''Event
        If mouse_click on element, execute its event, of not null'''
        if self.show_mouse:
            show_mouse()
            mouse_pos, pressed = get_mouse()
            if pressed[0] and not self.click:
                event = None
                self.click = True
                if not self.dialog:
                    for layer in self.images:
                        for image in layer:
                            if image.check_click(mouse_pos,self.screen_pos):
                                event = image.event
                else:
                    
                    if self.dialog_text2.time >= self.dialog_text2.gradient:
                        if len(self.dialog_answers) == 0:
                            self.dialog = False
                            self.dialog_event.answer()
                        for i in range(len(self.dialog_answers)):
                            if self.dialog_answers[i].check_click(mouse_pos,self.screen_pos):
                                self.dialog = False
                                self.dialog_event.answer(self.answer_text[i].text)
                                break
                    else:
                        self.dialog_text.end_gradient()
                        self.dialog_text2.end_gradient()
                        
                if event:
                    event.execute()
            elif not pressed[0]:
                self.click = False
        '''Dialog'''
        if self.dialog and not self.editor:
            show_mouse()
            if self.dialog_text.time >= self.dialog_text.gradient:
                for button in self.dialog_answers:
                    '''show answers'''
                    button.loop(screen,self.screen_pos)
                for answer in self.answer_text:
                    answer.loop(screen,self.screen_pos)
            self.dialog_box.loop(screen, self.screen_pos)
            self.dialog_text.loop(screen, self.screen_pos)
            if self.dialog_text.time >= self.dialog_text.gradient:
                self.dialog_text2.loop(screen, self.screen_pos)