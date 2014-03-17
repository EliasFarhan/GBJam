'''
Created on 17 mars 2014

@author: efarhan
'''
from engine.stat import egal_condition, set_value, get_value
from engine.sound_manager import load_sound, play_sound, set_playlist
from json_export.json_main import get_element
from engine.const import log
from json_export.event_json import parse_event_json
from engine.level_manager import get_level

class Event():
    def __init__(self):
        self.parent_event = None # for dialog only
        self.next_event = None
    def set_parent_event(self,parent_event):
        self.parent_event = parent_event
        if self.next_event == None:
            self.next_event = parent_event.next_event
    def execute(self):
        if self.next_event:
            self.next_event.execute()
        #for dialog tree only
        elif self.parent_event:
            if self.parent_event.next_event:
                self.parent_event.next_event.execute()
    @staticmethod
    def parse_event(event_dict):
        return Event()




class DialogEvent(Event):
    def __init__(self,gamestate,text,text2=""):
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


class SwitchEvent(Event):
    def __init__(self,gamestate,new_level_name):
        Event.__init__(self)
        self.gamestate = gamestate
        self.filename = new_level_name
    def execute(self):
        self.gamestate.reload(self.filename)
        Event.execute(self)
    @staticmethod
    def parse_event(event_dict):
        new_level_name = get_element(event_dict,"name")
        if new_level_name:
            return SwitchEvent(get_level(),new_level_name)
        else:
            log("Invalid arg name for SwitchEvent")
class SoundEvent(Event):
    def __init__(self,sound_name):
        Event.__init__(self)
        self.sound_name = sound_name
        self.sound = load_sound(sound_name)
    def execute(self):
        play_sound(self.sound)
        Event.execute(self)
    @staticmethod
    def parse_event(event_dict):
        path = get_element(event_dict,"path")
        if path:
            return SoundEvent(path)
        else:
            log("Invalid arg path for SoundEvent",1)
            return None

class MusicEvent(Event):
    def __init__(self,playlist):
        Event.__init__(self)
        self.playlist = playlist
    def execute(self):
        set_playlist(self.playlist)
        Event.execute(self)
    @staticmethod
    def parse_event(event_dict):
        new_playlist = get_element(event_dict, "playlist")
        if new_playlist:
            return MusicEvent(new_playlist)
        else:
            log("Invalid arg playlist for MusicEvent",1)
            return None

class VisualEvent(Event):
    def __init__(self,gamestate,name="",names=[],pos=None,next_pos=None,size=1):
        self.gamestate = gamestate
        self.name = name
        self.names = names
        

        self.pos = pos
        self.next_pos = next_pos
        self.size = size
        Event.__init__(self)
    def change(self,names=[]):
        for name in names:
            
            self.gamestate.characters[name].index = self.size
            if self.pos:
                self.gamestate.characters[name].pos = self.pos
            if self.next_pos:
                self.gamestate.characters[name].next_pos = self.next_pos
            self.gamestate.characters[name].update_rect()
    def execute(self):
        if self.name != "":
            self.change([self.name])
        elif self.names != []:
            self.change(self.names)
        Event.execute(self)
    @staticmethod
    def parse_event(event_dict):
        return Event.parse_event(event_dict)
class ConditionnalEvent(Event):
    def __init__(self,name,value,event1,event2):
        Event.__init__(self)
        self.name = name
        self.value = value
        self.if_event = event1
        self.else_event = event2
    def execute(self):
        if egal_condition(self.name,self.value):
            if self.if_event:
                self.if_event.execute()
        else:
            if self.else_event:
                self.else_event.execute()
    @staticmethod
    def parse_event(event_dict):
        name = get_element(event_dict, "name")
        value = get_element(event_dict,"value")
        if not (name and value):
            log("Invalid arg name and value for ConditionnalEvent",1)
            return None
        if_event = None
        if_event_dict = get_element(event_dict, "if_event")
        if if_event_dict:
            if_event = parse_event_json(if_event_dict)
        else_event = None
        else_event_dict = get_element(event_dict, "else_event")
        if else_event_dict:
            else_event = parse_event_json(else_event_dict)
        return ConditionnalEvent(name, value, if_event, else_event)
class IncreaseValueEvent(Event):
    def __init__(self,name):
        Event.__init__(self)
        self.name = name
    def execute(self):
        set_value(self.name, get_value(self.name)+1)
        Event.execute(self)
    @staticmethod
    def parse_event(event_dict):
        value_name = get_element(event_dict, "name")
        if value_name:
            return IncreaseValueEvent(value_name)
        else:
            log("Invalid arg for IncreaseValueEvent",1)
            return None
class SetValueEvent(Event):
    def __init__(self,name,value):
        Event.__init__(self)
        self.name = name
        self.value = value
    def execute(self):
        set_value(self.name, self.value)
        Event.execute(self)
    @staticmethod
    def parse_event(event_dict):
        value_name = get_element(event_dict, "name")
        new_value = get_element(event_dict, "value")
        if value_name and new_value:
            return SetValueEvent(value_name,new_value)
        else:
            log("Invalid arg for IncreaseValueEvent",1)
            return None
'''
def parse_change_image_event(event_dict,parent_event=None,object=None):
    event = ChangeImageEvent(get_level(), event_dict["name"], event_dict["path"])
    try:
        event.next_event = parse_event_json(event_dict["next_event"])
    except KeyError:
        pass
    return event


def parse_dialog_event(event_dict,parent_event=None,object=None):
    text2 = ""
    try:
        text2 = event_dict["text2"]
    except KeyError:
        pass
    event = DialogEvent(get_level(), event_dict["text"],text2)
    try:
        event.next_event = parse_event_json(event_dict["next_event"])
        if not event.next_event:
            if parent_event:
                event.next_event = parent_event.next_event
    except KeyError:
        pass
    try:
        answers = {}
        for answer in event_dict['answers'].keys():
            answers[answer] = parse_event_json(event_dict['answers'][answer], event, object)
        event.set_answers(answers)
    except KeyError:
        pass
    return event
    
def parse_visual_event(event_dict,parent_event=Nonew_level_name ne,object=None):
    pos = None
    try:
        pos = event_dict["pos"]
    except KeyError:
        pass
    next_pos = None
    try:
        next_pos = event_dict["next_pos"]
    except KeyError:
        pass
    size = 1
    try:
        size = event_dict["size"]
    except KeyError:
        pass
    name = ""
    try:
        name = event_dict["name"]
    except KeyError:
        pass
    names = []
    try:
        names = event_dict["names"]
    except KeyError:
        pass
    event = VisualEvent(get_level(), name, names, pos, next_pos, size)
    try:
        event.next_event = parse_event_json(event_dict["next_event"])
    except KeyError:
        pass
    return event'''