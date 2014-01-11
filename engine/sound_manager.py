import pygame

sounds = {}
sounds_indexes = {}
sound_index = 0
playlist = []
music_index = 0
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
	global sounds, sounds_indexes, sound_index
	try:
		sounds_indexes[name]
	except KeyError:
		sounds[sound_index] = pygame.mixer.Sound(name)
		sounds_indexes[name] = sound_index
		sound_index+=1
		return sound_index-1
	return sounds_indexes[name]

def play_sound(index):
	global sounds
	sounds[index].play()


