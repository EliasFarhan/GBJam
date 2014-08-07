from engine.const import log
from event.event_engine import Event
from json_export.json_main import get_element
from render_engine.snd_manager import snd_manager

__author__ = 'efarhan'


class SoundEvent(Event):
    def __init__(self,sound_name):
        Event.__init__(self)
        self.sound_name = sound_name
        self.sound = snd_manager.load_sound(sound_name)

    def execute(self):
        snd_manager.play_sound(self.sound)
        Event.execute(self)

    @staticmethod
    def parse_event(event_dict):
        path = get_element(event_dict, "path")
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
        snd_manager.set_playlist(self.playlist)
        Event.execute(self)

    @staticmethod
    def parse_event(event_dict):
        new_playlist = get_element(event_dict, "playlist")
        if new_playlist:
            return MusicEvent(new_playlist)
        else:
            log("Invalid arg playlist for MusicEvent",1)
            return None