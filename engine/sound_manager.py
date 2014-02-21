from engine.const import pookoo, log
from engine.event import Event
if not pookoo:
	import pygame

sounds = {}
playlist = []
music_index = 0

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

def set_playlist(music_list):
	global playlist
	log("YOLO")
	playlist = music_list
	pygame.mixer.music.load(playlist[0])
	pygame.mixer.music.play()
	
def add_music_to_playlist(self,name):
	global playlist
	playlist.append(name)

def fadeout_music(t=0):
	if(pygame.mixer.music.get_busy()):
		if(t != 0):
			pygame.mixer.music.fadeout(t)
		else:
			pygame.mixer.music.fadeout(1)

def play_music(name):
	global playlist
	playlist = [name]
	pygame.mixer.music.load(playlist[0])
	pygame.mixer.music.play()
	
def update_music_status():
	global music_index,playlist
	if(not pygame.mixer.music.get_busy()):
		if(music_index != len(playlist)-1):
			music_index += 1
		else:
			music_index = 0
		pygame.mixer.music.load(playlist[music_index])
		pygame.mixer.music.play()
		
def check_music_status():
	return pygame.mixer.music.get_busy()

def load_sound(name):
	global sounds
	try:
		sounds[name]
	except KeyError:
		sounds[name] = pygame.mixer.Sound(name)
	return sounds[name]

def play_sound(sound):
	log("Play sound")
	sound.play()


