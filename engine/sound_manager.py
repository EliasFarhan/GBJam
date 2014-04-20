"""
Manage sound and music
"""

from engine.const import log, CONST

if CONST.render == 'sfml':
    import sfml
elif CONST.render == 'pookoo':
    import pookoo.audio
sounds = {}
permanent_sound = []
playlist = []
music_index = 0
music = None
sounds_playing = []


def set_playlist(music_list):
    """
    Set a new playlist and play the first element
    """
    global playlist, music
    playlist = music_list
    if CONST.render == 'sfml':
        music = sfml.Music.from_file(playlist[0])
        music.play()
    elif CONST.render == 'pookoo':
        pass


def add_music_to_playlist(self, name):
    """
	Add a music at the end of the playlist
	"""
    global playlist
    playlist.append(name)


def fadeout_music(t=0):
    """TODO: Fadeout and then stop it after time t (seconds)"""


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
        if music.status == sfml.Music.STOPPED:
            music_index += 1
            music_index = music_index % len(playlist)
            music = sfml.Music.from_file(playlist[music_index])
            music.play()
        delete_sounds = []
        for s in sounds_playing:
            if s.status == sfml.Sound.STOPPED:
                delete_sounds.append(s)
        for s in delete_sounds:
            sounds_playing.remove(s)
        del delete_sounds[:]


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


