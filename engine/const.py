'''
Created on 8 sept. 2013

@author: efarhan
'''
import sys
#constant for physics and gameplay

cuted_size = (500,500)
debug = True
gravity = 20
move_speed = 2
jump = 10 #8.5
jump_step = 5
framerate = 60
animation_step = 12
invulnerability = 60
pybox2d = False
if sys.platform == 'darwin':
	jump_step = 4
	framerate = 30
	animation_step = 3
	invulnerability = 30

startup = "gameplay"
def log(text):
	sys.stdout.write(str(text)+"\n")
