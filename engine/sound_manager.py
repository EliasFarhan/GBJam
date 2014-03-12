'''
Manage sound and music 
'''

from engine.const import log, render
from pygame.mixer import music
if render == 'pygame':
	import pygame
elif render == 'sfml':
	import sfml

sounds = {}
permanent_sound = []
playlist = []
music_index = 0
music = None
sounds = []

def set_playlist(music_list):
	'''
	Set a new playlist and play the first element
	'''
	global playlist,music
	log("YOLO")
	playlist = music_list
	if render == 'pygame':
		pygame.mixer.music.load(playlist[0])
		pygame.mixer.music.play()
	elif render == 'sfml':
		music = sfml.Music.from_file(playlist[0])
		music.play()
def add_music_to_playlist(self,name):
	'''
	Add a music at the end of the playlist
	'''
	global playlist
	playlist.append(name)

def fadeout_music(t=0):
	'''Fadeout and then stop it after time t (seconds)'''
	if(pygame.mixer.music.get_busy()):
		if(t != 0):
			pygame.mixer.music.fadeout(t)
		else:
			pygame.mixer.music.fadeout(1)

def play_music(name):
	'''
	Set the playlist as one element and play it
	'''
	global playlist
	set_playlist([name])
	
def update_music_status():
	'''
	Switch to next music if it's over,
	must be called to have smooth transition
	'''
	global music,music_index,playlist
	if render == 'pygame':
		if(not pygame.mixer.music.get_busy()):
			music_index += 1
			music_index = music_index%len(playlist)
			pygame.mixer.music.load(playlist[music_index])
			pygame.mixer.music.play()
	elif render == 'sfml':
		if music.status == sfml.Music.STOPPED:
			music_index += 1
			music_index = music_index%len(playlist)
			music = sfml.Music.from_file(playlist[music_index])
			music.play()
		for s in sounds:
			if s.status == sfml.Sound.STOPPED:
				'''TODO: remove sound'''
				pass
def check_music_status():
	'''
	Return True if a music is currently playing
	'''
	if render == 'pygame':
		return pygame.mixer.music.get_busy()
	elif render == 'sfml':
		return music.status == sfml.Music.STOPPED

def load_sound(name,permanent=False):
	'''Load a sound in the system and returns it'''
	global sounds,permanent_sound
	try:
		sounds[name]
	except KeyError:
		if render == 'pygame':
			sounds[name] = pygame.mixer.Sound(name)
		elif render == 'sfml':
			sounds[name] = sfml.SoundBuffer.from_file(name)
	if permanent:
		permanent_sound.append(name)
	return sounds[name]

def play_sound(sound):
	'''
	Plays a given sound
	'''
	if render == 'pygame':
		sound.play()
	elif render == 'sfml':
		sfml.Sound(sound).play()


