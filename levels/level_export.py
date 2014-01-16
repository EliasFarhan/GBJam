'''
Created on 11 janv. 2014

@author: efarhan
'''
import json
from game_object.player import Player

def load_level(level):
    file = None
    try:
        file = open(level.filename, mode='r')
    except FileNotFoundError:
        return False
    level_data = None
    try:
        level_data = json.loads(file.read())
    except ValueError: #No json object decoded
        return False
    ''' 
    TODO: Import a level with:
    
    -Physics static object
    -Images with or without animation
    -IA (if any)
    -Player position, size, etc... but not recreate the player!!!
    '''
    
    level.player = Player(level_data['player'])
    
    
    file.close()
    return True
def save_level(level):
    file = open(level.filename,mode='w')
    
    
    
    file.close()