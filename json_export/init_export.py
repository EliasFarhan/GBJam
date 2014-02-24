'''
Created on Feb 24, 2014

@author: efarhan
'''
from json_export.json_export import load_json


def load_init_file(path):
    init_data = load_json(path)
    screen_size = init_data["screen_size"]
    startup = init_data["startup"]
    return screen_size, startup