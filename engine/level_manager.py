from levels.logo_kwakwa import Kwakwa as logo_kwakwa
from levels.logo_pygame import Pygame as logo_pygame
from levels.main_menu import MainMenu as main_menu
from levels.gameplay import GamePlay as gameplay
from levels.level1 import Level1 as level1
from levels.theend import TheEnd as the_end
dict_level = { "logo_kwakwa" : logo_kwakwa, "logo_pygame" : logo_pygame,\
			 "main_menu" : main_menu, "gameplay": gameplay, "level1":level1, "TheEnd":the_end }

level = 0
def switch(level_name):
	global level
	try:
		level = dict_level[level_name]()
	except KeyError:
		level = 0
	if level != 0:
		level.init()
def function_level():
	if level == 0:
		return level
	return level.loop
