'''
Created on Feb 24, 2014

@author: efarhan
'''
from json_export.json_main import load_json


def load_init_file(path):
    '''
    Set init value from JSON file
    '''
    init_data = load_json(path)
    screen_size = [1280,720]
    startup = ''
    try:
        screen_size = init_data["screen_size"]
        startup = init_data["startup"]
    except TypeError:
        pass
    return screen_size, startup