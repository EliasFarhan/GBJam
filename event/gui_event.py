from engine.level_manager import get_level
from event.event_engine import Event
from json_export.event_json import load_event, parse_event_json
from json_export.json_main import get_element

__author__ = 'efarhan'


class DialogEvent(Event):
    def __init__(self, gamestate, text, text2=""):
        Event.__init__(self)
        self.text = text
        self.text2 = text2
        self.answers = {}
        self.gamestate = gamestate

    def set_answers(self,answers):
        self.answers = answers

    def execute(self):
        self.gamestate.dialog = True
        self.gamestate.dialog_text.set_text(self.text)
        self.gamestate.dialog_text2.set_text(self.text2)

        self.gamestate.set_answers(self.answers.keys())
        self.gamestate.dialog_event = self

    def answer(self, answer=None):
        self.gamestate.dialog = False
        new_event = None
        if answer:
            new_event = self.answers[answer]

        if new_event:
            new_event.execute()
        else:
            Event.execute(self)

    @staticmethod
    def parse_event(event_dict):
        """Dynamic parsing of DialogEvent"""
        text = get_element(event_dict,"text")
        if text is None:
            return None
        text2 = get_element(event_dict,"text2")
        if text2 is None:
            text2 = ''

        dialog_event = DialogEvent(get_level(),text,text2)
        answers = get_element(event_dict, "answers")
        if answers is not None:
            for answer_key in answers:
                answers[answer_key] = parse_event_json(answers[answer_key]) #TODO: add parent event?
            dialog_event.set_answers(answers)

        return Event.parse_event(event_dict)