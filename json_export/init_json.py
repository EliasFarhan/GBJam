'''
Created on Feb 24, 2014

@author: efarhan
'''
import os
from json_export.json_main import load_json, write_json, get_element
from engine.const import path_prefix
from json_export.key_json import load_key_json


def load_init_file(path):
    '''
    Set init value from JSON file
    '''
    init_data = load_json(path_prefix+path)
    if init_data == None:
        path_directories = path.split('/')
        length = len(path_directories)
        for i in range(length-1):
            if not os.path.isdir(path_prefix+"/".join(path_directories[0:i])):
                os.mkdir(path_prefix+"/".join(path_directories[0:i]))
        
        init_data = {'screen_size': [1280,720],'startup' : ''}
        if write_json(path_prefix+path, init_data):
            init_data = load_json(path_prefix+path)
    screen_size = init_data["screen_size"]
    startup = init_data["startup"]
    fullscreen = get_element(init_data, "fullscreen")
    if fullscreen == None:
        fullscreen = False
    action_data = get_element(init_data,"actions")
    if action_data:
        if type(action_data) == dict:
            load_key_json(action_data)
        elif type(action_data) == unicode:
            load_key_json(load_json(action_data))
    return [screen_size, startup, fullscreen]