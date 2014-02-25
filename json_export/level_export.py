'''
Created on 11 janv. 2014

@author: efarhan
'''
import json
from game_object.player import Player
from game_object.physic_object import AngleSquare
from engine.const import log,path_prefix
from game_object.image import Image
from json_export.json_export import load_json
from json_export.event_export import load_event

def load_level(level):
    ''' 
    Import a level with:
    
    -Physics static object
    -Images with or without animation
    -IA (if any)
    -Player position, size, etc... but not recreate the player!!!
    '''
    level_data = load_json(level.filename)
    if level_data:
        level.player = Player(path_prefix+level_data['player'])
        level.bg_color = level_data['background_color']
        try:
            level.show_mouse = level_data['show_mouse']
        except KeyError:
            pass
        try:
            level.use_physics = level_data['physics']
        except KeyError:
            pass
        try:
            level.use_network = level_data['network']
        except KeyError:
            pass
        
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
        for image_data in level_data['images']:
            if image_data["type"] == "Image":
                pos = image_data["pos"]
                size = None
                try:
                    size = image_data["size"]
                except KeyError:
                    pass
                path = path_prefix+image_data["path"]
                try:
                    angle = image_data["angle"]
                except KeyError:
                    pass
                layer = image_data["layer"]
                image = Image(path, pos, None, size, angle)
                try:
                    event_path = image_data["event"]
                    image.event = load_event(event_path)
                except KeyError:
                    pass
                if 0 < layer < len(level.images)-1:
                    level.images[layer-1].append(image)
        return True
    return False
def save_level(level):
    
    
    level_data = {}
    level_data['player'] = level.player.filename
    level_data['background_color'] = level.bg_color
    level_data['physic_objects'] = []
    for physic_object in level.physic_objects:
        if physic_object.__class__ == AngleSquare:
            obj = {}
            obj['type'] = 'box'
            obj['pos'] = [physic_object.pos[0],physic_object.pos[1]]
            obj['size'] = [physic_object.size[0],physic_object.size[1]]
            obj['sensor'] = physic_object.sensor
            obj['user_data'] = physic_object.data
            obj['angle'] = physic_object.angle
            level_data['physic_objects'].append(obj)
    i = 1 #layer
    level_data['images'] = []
    for layer in level.images:
        for image in layer:
            obj = {}
            obj['type'] = 'Image'
            obj['layer'] = i
            obj['path'] = image.path
            obj['size'] = [image.size[0],image.size[1]]
            obj['pos'] = [image.pos[0],image.pos[1]]
            obj['angle'] = image.angle
            level_data['images'].append(obj)
        i+=1
    file = open(level.filename,mode='w')
    file.write(json.dumps(obj=level_data,indent=4))
    file.close()