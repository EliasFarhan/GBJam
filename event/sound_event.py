'''
Created on Feb 26, 2014

@author: efarhan
'''
from event.event import Event
from engine.sound_manager import load_sound, play_sound, set_playlist


class SoundEvent(Event):
    def __init__(self,sound_name):
        Event.__init__(self)
        self.sound_name = sound_name
        self.sound = load_sound(sound_name)
    def execute(self):
        play_sound(self.sound)
        Event.execute(self)

class MusicEvent(Event):
    def __init__(self,playlist):
        Event.__init__(self)
        self.playlist = playlist
    def execute(self):
        set_playlist(self.playlist)
        Event.execute(self)
