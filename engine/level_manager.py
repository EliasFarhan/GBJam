

level = 0

def switch_level(level_obj):
	global level
	from engine.loop import get_console
	
	level = level_obj
	c = get_console()
	c.submit_input('''import __main__;current_scene = __main__.game.level_manager.get_level()''')
	if level != 0:
		level.init()
def function_level():
	global level
	if level == 0:
		return level
	return level.loop

def get_level():
	global level
	return level