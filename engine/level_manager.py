"""
Abstraction of the loop function
providing the level
"""

from engine.const import CONST

level = 0


def switch_level(level_obj):
    global level

    level = level_obj
    if level != 0:
        CONST.parse_const(CONST.path_prefix+"data/json/init.json")
        level.init()


def update_level():
    global level
    if level == 0:
        return level
    return level.loop


def get_level():
    global level
    return level