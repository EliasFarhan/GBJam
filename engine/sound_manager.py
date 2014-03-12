'''
Manage sound and music 
'''

from engine.const import log, render
if render == 'pygame':
	import pygame
elif render == 'sfml':
	import sfml

sounds = {}
permanent_sound = []
playlist = []
music_index = 0

def set_playlist(music_list):
	'''
	Set a new playlist and play the first element
	'''
	global playlist
	log("YOLO")
	playlist = music_list
	pygame.mixer.music.load(playlist[0])
	pygame.mixer.music.play()
	
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
	global music_index,playlist
	if(not pygame.mixer.music.get_busy()):
		if(music_index != len(playlist)-1):
			music_index += 1
		else:
			music_index = 0
		pygame.mixer.music.load(playlist[music_index])
		pygame.mixer.music.play()
		
def check_music_status():
	'''
	Return True if a music is currently playing
	'''
	return pygame.mixer.music.get_busy()

def load_sound(name,permanent=False):
	'''Load a sound in the system and returns it'''
	global sounds,permanent_sound
	try:
		sounds[name]
	except KeyError:
		sounds[name] = pygame.mixer.Sound(name)
	if permanent:
		permanent_sound.append(name)
	return sounds[name]

def play_sound(sound):
	'''
	Plays a given sound
	'''
	sound.play()


