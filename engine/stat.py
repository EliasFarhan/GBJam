'''
Stat is used to dynamically set value
in a gamestate

TODO: save those values when saving game

Created on 22 fevr. 2014

@author: efarhan
'''

from engine.const import log
values = {}

def egal_condition(name,v):
    try:
        return get_value(name) == v
    except KeyError:
        return False
    
def greater_condition(name,v):
    try:
        return get_value(name) > v
    except KeyError:
        return False
    
def lesser_condition(name,v):
    try:
        return get_value(name) < v
    except KeyError:
        return False

def set_value(name,v):
    values[name] = v

def get_value(name):
    try:
        return values[name]
    except KeyError:
        return None
    
