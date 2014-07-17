"""
Manage sound and music
"""

from engine.const import CONST

snd_manager = None


class SndManager():
    def __init__(self):
        self.sounds = {}
        self.permanent_sound = []
        self.playlist = []
        self.music_index = 0
        self.music = None
        self.sounds_playing = []

    def set_playlist(self,music_list):
        pass

    def add_music_to_playlist(self, name):
        pass

    def play_music(self,name):
        pass

    def update_music_status(self):
        pass

    def sanitize_sounds(self,delete_sounds=[]):
        del_snd_tmp = []
        if delete_sounds == []:
            for snd_filename in self.sounds.keys():
                if snd_filename not in self.permanent_sound:
                    del_snd_tmp.append(snd_filename)
        else:
            del_snd_tmp = delete_sounds
        for snd_filename in del_snd_tmp:
            del self.sounds[snd_filename]

snd_manager = SndManager()

if CONST.render == 'sfml':
    from render_engine.sfml_engine.sfml_snd_manager import SFMLSndManager
    snd_manager = SFMLSndManager()
'''
elif CONST.render == 'pookoo':


def set_playlist(music_list):
    """
    Set a new playlist and play the first element
    """
    global playlist, music

    music = pookoo.audio.AudioStreamObject(playlist[0])


def add_music_to_playlist(self, name):
    """
    Add a music at the end of the playlist
    """
    global playlist
    playlist.append(name)


def fadeout_music(t=0):
    """TODO: Fadeout and then stop it after time t (seconds)"""
    pass

def play_music(name):
    """
	Set the playlist as one element and play it
	"""
    global playlist
    set_playlist([name])


def update_music_status():
    """
	Switch to next music if it's over,
	must be called to have smooth transition
	"""
    global music, music_index, playlist, sounds_playing
    if CONST.render == 'sfml':
        pass


def check_music_status():
    """
	Return True if a music is currently playing
	"""
    global music
    if CONST.render == 'sfml':
        return music.status == sfml.Music.STOPPED


def load_sound(name, permanent=False):
    """Load a sound in the system and returns it"""
    global sounds, permanent_sound
    try:
        sounds[name]
    except KeyError:
        if CONST.render == 'sfml':
            sounds[name] = sfml.SoundBuffer.from_file(name)
        elif CONST.render == 'pookoo':
            sounds[name] = pookoo.audio.AudioSoundObject(name)
    if permanent:
        permanent_sound.append(name)
    return sounds[name]


def play_sound(sound):
    """
	Plays a given sound
	"""
    global sounds_playing
    if CONST.render == 'sfml':
        sound_playing = sfml.Sound(sound)
        sound_playing.play()
        sounds_playing.append(sound_playing)
'''



