'''
Created on 8 sept. 2013

@author: efarhan
'''

import sys
from json_export.init_json import load_init_file
#constant for physics and gameplay

render = 'pygame'

def log(text,error=0):
	"""
	Log a message into the stdout or the stdin
	"""
	if error == 0:
		sys.stdout.write(str(text)+"\n")
	else:
		sys.stderr.write(str(text)+"\n")


path_prefix = ""

try:
	import sfml
	
	render = 'sfml'
except ImportError:
	try:
		import pygame
	except ImportError:
		log("pygame or pysfml should be installed",1)

try:
	import Box2D
except ImportError:
	log('Box2D should be installed',1)
	

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


