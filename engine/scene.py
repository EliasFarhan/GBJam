from engine.image_manager import sanitize_img_manager
class Scene():
	def __init__(self):
		pass
	def init(self):
		pass
	def loop(self, screen):
		pass
	def exit(self,screen):
		sanitize_img_manager()