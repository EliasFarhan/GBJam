
level = 0

def switch_level(level_obj):
	global level
	level = level_obj
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