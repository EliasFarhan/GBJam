'''
Created on Feb 26, 2014

@author: efarhan
'''
from engine.const import log

from engine.init import get_screen_size
from engine.vector import Vector2
from game_object.text import Text
from game_object.image import Image
from event.mouse_event import show_mouse, get_mouse


class GUI():
    def __init__(self):
        self.dialog = False

        self.answers_text = []
        self.answers_image = []
        self.dialog_event = None

        self.dialog_box_image = 'data/sprites/gui/dialog_box.png'

        self.show_mouse = True

        self.dialog_font = "data/font/pixel_arial.ttf"
        self.dialog_y_size = 1.0 / 3.0
        self.answer_size = Vector2(1.0 / 4.0, 1.0 / 6.0)
        self.dialog_margin = 0.05
        self.answer_margin = 0.0
        self.gui_click = False
        self.init_dialog_text()

    def init_dialog_text(self):
        self.dialog_text = Text(pos=get_screen_size()*Vector2(self.dialog_margin,1-self.dialog_y_size+self.dialog_margin),
                                size=get_screen_size()*Vector2(1-2*self.dialog_margin,self.dialog_y_size/2-1.5*self.dialog_margin).y,
                                font=self.dialog_font,
                                text="",
                                relative=True)
        self.dialog_text2 = Text(pos=get_screen_size()*Vector2(self.dialog_margin,1-self.dialog_y_size/2+self.dialog_margin),
                                 size=get_screen_size()*Vector2(1-2*self.dialog_margin,self.dialog_y_size/2-1.5*self.dialog_margin).y,
                                 font=self.dialog_font,
                                 text="",
                                 relative=True)
        self.dialog_box = Image(path=self.dialog_box_image,
                                pos=(get_screen_size()*Vector2(0,1-self.dialog_y_size)).get_tuple(),
                                size=(get_screen_size()*Vector2(1.0, self.dialog_y_size)).get_tuple(),
                                relative=True)

    def set_dialog(self, text, text2=''):
        pass

    def set_answers(self, answers):
        del self.answers_text[:]
        del self.answers_image[:]
        i = 0
        answer_nmb = len(answers)
        for answer in answers:

            pos = (get_screen_size()*Vector2((1 - self.answer_size.x), ((1 - self.dialog_y_size) - (answer_nmb - i) * self.answer_size.y)))
            size = (get_screen_size()*Vector2(self.answer_size.x, self.answer_size.y))
            self.answers_text.append(Text(pos=pos, size=size.y, font=self.dialog_font, text=answer, relative=True))
            if self.dialog_box_image:
                self.answers_image.append(Image(self.dialog_box_image, pos, size=size, relative=True))
            i += 1

    def loop(self, screen):
        """Loop of the GUI part of the Gamestate"""

        '''Event
        If mouse_click on element, execute its event, of not null'''
        if self.show_mouse:
            show_mouse()
            mouse_pos, pressed = get_mouse()
            if pressed[0] and not self.gui_click:
                event = None
                self.gui_click = True
                if not self.dialog:
                    for layer in self.images:
                        for image in layer:
                            if image.check_click(mouse_pos, self.screen_pos):
                                event = image.event
                else:
                    if self.dialog_text2.time >= self.dialog_text2.gradient:
                        if len(self.answers_image) == 0:
                            self.dialog = False
                            self.dialog_event.answer()
                        for i, answer_image in enumerate(self.answers_image):

                            if answer_image.check_click(mouse_pos, self.screen_pos):
                                self.dialog = False
                                self.dialog_event.answer(self.answers_text[i].text)
                                break
                    else:
                        self.dialog_text.end_gradient()
                        self.dialog_text2.end_gradient()

                if event:
                    event.execute()
            elif not pressed[0]:
                self.gui_click = False
        '''Dialog'''
        if self.dialog and self.dialog_text and not self.editor:
            show_mouse()
            if self.dialog_text.time >= self.dialog_text.gradient:
                for button in self.answers_image:
                    '''show answers'''
                    button.loop(screen, self.screen_pos)
                for answer in self.answers_text:
                    answer.loop(screen, self.screen_pos)
            self.dialog_box.loop(screen, self.screen_pos)
            self.dialog_text.loop(screen, self.screen_pos)
            if self.dialog_text.time >= self.dialog_text.gradient:
                self.dialog_text2.loop(screen, self.screen_pos)

    @staticmethod
    def load_gui_json(json_dict, level):
        pass