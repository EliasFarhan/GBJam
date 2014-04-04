from event.event_engine import Event

__author__ = 'efarhan'

class DialogEvent(Event):
    def __init__(self, gamestate,text,text2=""):
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
    def answer(self,answer=None):
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
        return Event.parse_event(event_dict)