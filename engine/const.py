"""
Created on 8 sept. 2013

@author: efarhan
"""

import sys
from json_export.json_main import load_json


def log(text, error=0):
    """
	Log a message into the stdout or the stdin
	"""
    if error == 0:
        sys.stdout.write(str(text) + "\n")
    else:
        sys.stderr.write(str(text) + "\n")


#constant for physics and gameplay
class CONST:
    path_prefix = ""
    render = ''
    debug = True
    gravity = 20
    move_speed = 2
    jump = 10  #8.5
    jump_step = 5
    framerate = 60
    fullscreen = False
    animation_step = 7
    startup = ""
    scale_speed = 0.01
    screen_size = [1920, 1080]
    string_type = None
    try:
        string_type = basestring
    except NameError:
        string_type = str
    @staticmethod
    def parse_const(init_filename):
        init_json = load_json(CONST.path_prefix + 'data/json/init.json')
        log(init_json)
        if init_json:
            for const in init_json.items():
                '''Check key'''
                char_check = True
                for c in const[0]:
                    if c != '_' and not c.isalpha():
                        char_check = False
                if char_check:
                    try:
                        log(str(const))
                        data = const[1]
                        if type(data) == CONST.string_type:
                            data = "'" + data + "'"
                        exec ("CONST.%s = %s" % (const[0], str(data)))
                    except Exception as e:
                        log("Error while setting value %s: " % (const[0]) + str(e), 1)
                        continue


try:
    import pookoo
except ImportError as e:
    log("Using pySFML, because Pookoo was not found")
    try:
        import sfml

        CONST.render = 'sfml'
    except ImportError as e:
        log("Error: could not load SFML: " + str(e), 1)
        exit()
try:
    import Box2D
except ImportError:
    log('Box2D should be installed', 1)
    exit()

CONST.parse_const('data/json/init.json')




