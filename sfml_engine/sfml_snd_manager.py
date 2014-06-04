import sfml
from engine.snd_manager import SndManager

__author__ = 'Elias'


class SFMLSndManager(SndManager):
    def __init__(self):
        SndManager.__init__(self)

    def add_music_to_playlist(self,new_playlist):
        pass

    def set_playlist(self,music_list):
        self.playlist = music_list
        self.music = sfml.Music.from_file(self.playlist[0])
        self.music.play()

    def update_music_status(self):
        if self.music.status == sfml.Music.STOPPED:
            self.music_index = (self.music_index + 1) % len(self.playlist)
            self.music = sfml.Music.from_file(self.playlist[self.music_index])
            self.music.play()
        delete_sounds = []
        for s in self.sounds_playing:
            if s.status == sfml.Sound.STOPPED:
                delete_sounds.append(s)
        for s in delete_sounds:
            self.sounds_playing.remove(s)
        del delete_sounds[:]

    def load_sound(self, name, permanent=False):
        """Load a sound in the system and returns it"""
        try:
            self.sounds[name]
        except KeyError:
            self.sounds[name] = sfml.SoundBuffer.from_file(name)
        if permanent:
            self.permanent_sound.append(name)
        return self.sounds[name]

    def play_sound(self, sound):
        """
        Plays a given sound
        """
        sound_playing = sfml.Sound(sound)
        sound_playing.play()
        self.sounds_playing.append(sound_playing)