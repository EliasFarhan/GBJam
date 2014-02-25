'''
Created on 8 sept. 2013

@author: efarhan
'''
import sys
from json_export.init_export import load_init_file
#constant for physics and gameplay

pybox2d = False
pookoo = False

path_prefix = ""

try:
	import window
	import log
	import texture
	import font
	import audio
	import draw
	import physics
	
	path_prefix = "../"
	pookoo = True
except ImportError:
	pass

try:
	import pypybox2d
except ImportError:
	pybox2d = True
try:
	import Box2D
	pybox2d=False
except ImportError:
	pybox2d=True
	

cuted_size = (500,500)
debug = True
gravity = 20
move_speed = 2
jump = 10 #8.5
jump_step = 5
framerate = 60
animation_step = 12


if sys.platform == 'darwin':
	jump_step = 4
	framerate = 30
	animation_step = 3
	invulnerability = 30

screen_size, startup = load_init_file(path_prefix+'data/json/init.json')

startup = path_prefix+startup

def log(text,error=0):
	"""
	Log a message into the stdout or the stdin
	"""
	if not pookoo:
		if error == 0:
			sys.stdout.write(str(text)+"\n")
		else:
			sys.stderr.write(str(text)+"\n")
	else:
		import log as log_module
		if error == 0:
			log_module.info(text)
		else:
			log_module.error(text)
