"""
Created on 8 sept. 2013

@author: efarhan
"""

import sys
from json_export.json_main import load_json


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


def log(text, error=0):
    """
    Log a message into the stdout or the stdin
    """
    if error == 0:
        if CONST.render != "pookoo":
            sys.stdout.write(str(text) + "\n")
            sys.stdout.flush()
        else:
            from pookoo import log as pookoo_log
            pookoo_log.info(str(text) + "\n")

    else:
        if CONST.render != "pookoo":
            sys.stderr.write(str(text) + "\n")
            sys.stderr.flush()
        else:
            from pookoo import log as pookoo_log
            pookoo_log.error(str(text) + "\n")


#constant for physics and gameplay
class CONST:
    """Engine CONSTANT"""
    """Core const"""
    render = ''
    physics = ''
    debug = False
    path_prefix = ""
    layers = 5
    animation_step = 7

    """Network"""
    network = False
    HOST = "eliasfarhan.ch"
    AUTH_PORT = 9999

    """Physics"""
    gravity = 0
    move_speed = 2
    jump = 13  #8.5
    jump_step = 1
    scale_speed = 0.01
    ratio = 100/1.5
    wall_jump = 10

    """Graphics"""
    framerate = 60
    fullscreen = False
    vsync = False


    startup = ""

    screen_size = [1920, 1080]

    """string_type for python2 and python3 compatibility"""
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
                        if isinstance(data, CONST.string_type):
                            data = "'" + data + "'"
                        exec("CONST.%s = %s" % (const[0], str(data)))
                    except Exception as e:
                        log("Error while setting value %s: " % (const[0]) + str(e), 1)
                        continue


try:
    import pookoo
    CONST.path_prefix = "../"
except ImportError:
    pass

CONST.parse_const(CONST.path_prefix+'data/json/init.json')

if CONST.render == 'sfml':
    try:
        import sfml
        log("Using pySFML")
        CONST.render = 'sfml'
    except ImportError as e:
        log("Error: could not load SFML: " + str(e), 1)
        sys.exit()
elif CONST.render == 'kivy':
    try:
        import kivy
        log("Using KIVY")
    except ImportError as e:
        log("Error: could not load KIVY: "+str(e),1)
        sys.exit()
elif CONST.render == 'pookoo':

    try:
        import pookoo
        log(str(pookoo)+" "+str(dir(pookoo)))
        CONST.path_prefix = "../"

    except ImportError as e:
        log("Error: could not load Pookoo: "+str(e),1)
        sys.exit()


if CONST.physics == 'b2':
    try:
        import Box2D
    except ImportError as e:
        log('Error: could not load Box2D '+str(e), 1)
        sys.exit()
elif CONST.physics == 'cymunk':
    try:
        import cymunk
    except ImportError as e:
        log('Error: could not load Cymunk '+str(e), 1)
        sys.exit()
elif CONST.physics == 'pookoo':
    try:
        import pookoo
        log(str(pookoo)+" "+str(dir(pookoo)))
        CONST.path_prefix = "../"

    except ImportError as e:
        log("Error: could not load Pookoo: "+str(e),1)
        sys.exit()