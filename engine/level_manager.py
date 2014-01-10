

level = 0

def switch_level(level_obj):
	global level
	level = level_obj
	if level != 0:
		level.init()
def function_level():
	if level == 0:
		return level
	return level.loop
