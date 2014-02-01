'''
Created on 11 janv. 2014

@author: efarhan
'''
import json
from game_object.player import Player
from game_object.physic_object import AngleSquare
from engine.const import log

def load_level(level):
    file = None
    try:
        file = open(level.filename, mode='r')
    except IOError:
        return False
    level_data = None
    try:
        level_data = json.loads(file.read())
    except ValueError as e: #No json object decoded
        log(e)
        return False
    ''' 
    Import a level with:
    
    -Physics static object
    -Images with or without animation
    -IA (if any)
    -Player position, size, etc... but not recreate the player!!!
    '''
    
    level.player = Player(level_data['player'])
    level.bg_color = level_data['background_color']
    for physic_object in level_data['physic_objects']:
        if physic_object["type"] == "box":
            
            pos = physic_object["pos"]
            size = physic_object["size"]
            
            sensor = False
            try:
                sensor = physic_object["sensor"]
            except KeyError:
                pass
            data = 0
            try:
                data = physic_object["user_data"]
            except KeyError:
                pass
            angle = 0
            try:
                angle = physic_object["angle"]
            except KeyError:
                pass
            level.physic_objects.append(AngleSquare(pos, size, angle, data, sensor))
    for image in level_data['images']:
        pass
    file.close()
    return True
def save_level(level):
    file = open(level.filename,mode='w')
    
    level_data = {}
    level_data['player'] = level.player.filename
    level_data['background_color'] = level.bg_color
    for physic_object in level.physic_objects:
        if physic_object.__class__ == AngleSquare:
            obj = {}
            obj['type'] = 'box'
            obj['pos'] = [physic_object.pos[0],physic_object.pos[1]]
            obj['size'] = [physic_object.size[0],physic_object.size[1]]
            obj['sensor'] = physic_object.sensor
            obj['user_data'] = physic_object.data
            obj['angle'] = physic_object.angle
            
    
    file.close()