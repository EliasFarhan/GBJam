'''
Created on 20 mars 2014

@author: efarhan
'''
from event.event_main import add_button


def load_key_json(key_json):
    if key_json:
        for key in key_json.items():
            add_button(key[0],key[1])