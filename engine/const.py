'''
Created on 8 sept. 2013

@author: efarhan
'''
import sys
#constant for physics and gameplay

pybox2d = False
pookoo = False

try:
	import window
	import log
	import texture
	import font
	import audio
	import draw
	import physics
	
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

startup = "gameplay"

def log(text):
	sys.stdout.write(str(text)+"\n")
