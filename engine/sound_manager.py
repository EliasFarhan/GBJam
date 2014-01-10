import pygame

class SoundManager():
	def __init__(self):
		sounds = {}
		self.playlist = []
		self.index = 0
	def add_music_to_playlist(self,name):
		self.playlist.append(name)
	def fadeout_music(self,t=0):
		if(pygame.mixer.music.get_busy()):
			if(t != 0):
				pygame.mixer.music.fadeout(t)
			else:
				pygame.mixer.music.fadeout(1)
	def play_music(self,name):
			
		self.playlist = [name]
		pygame.mixer.music.load(self.playlist[0])
		pygame.mixer.music.play()
	def update_music_status(self):
		if(not pygame.mixer.music.get_busy()):
			if(self.index != len(self.playlist)):
				self.index += 1
			else:
				self.index = 0
			pygame.mixer.music.load(self.playlist[self.index])
			pygame.mixer.music.play()
	def check_music_status(self):
		return pygame.mixer.music.get_busy()
	def load(self, name):
		pass
	
	def play(self, name):
		pass


snd_manager = SoundManager()