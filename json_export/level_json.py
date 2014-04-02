'''
Created on 11 janv. 2014

@author: efarhan
'''
import json

from engine.const import log,CONST
from game_object.image import Image, AnimImage
from json_export.json_main import load_json, get_element, write_json
from json_export.event_json import load_event
from game_object.text import Text
from game_object.game_object_main import GameObject
from engine.physics import add_dynamic_object, add_static_box, add_static_object
from json_export.image_json import load_image_from_json, reset_object_id


def load_level(level):
    """
    Import a level with:

    -Physics static object
    -Images with or without animation
    -IA (if any)
    -Player position, size, etc... but not recreate the player!!!
    """
    level_data = load_json(level.filename)
    if level_data:
        player_data = get_element(level_data, 'player')
        if player_data:
            '''load the json containing the player
            and treat it as an AnimImage'''
            player = None
            if type(player_data) == unicode:
                player_json = load_json(CONST.path_prefix+player_data)
                player = load_image_from_json(player_json, level, "AnimImage")
            elif type(player_data) == dict:
                player = load_image_from_json(player_data, level, "AnimImage")
            
            if player:
                level.player = player
        bg_color = get_element(level_data,'bg_color')
        if bg_color is not None:
            level.bg_color = bg_color
        show_mouse = get_element(level_data,'show_mouse')
        if show_mouse is not None:
            level.show_mouse = show_mouse
        
        use_physics = get_element(level_data,'use_physics')
        if use_physics is not None:
            level.use_physics = use_physics
        network = get_element(level_data, 'network')
        if network is not None:
            level.use_network = network
        
        event_data = get_element(level_data, "event")
        if event_data:
            for e in event_data.keys():
                level.event[e] = load_event(event_data[e])

        objects_dict = get_element(level_data, 'objects')
        reset_object_id()
        if objects_dict is not None:
            for object_data in objects_dict:
                if type(object_data) == unicode:
                    load_image_from_json(load_json(object_data), level, None)
                
                elif type(object_data) == dict:
                    image_type = get_element(object_data,"type")
                    load_image_from_json(object_data,level,image_type)
        return True
    return False


def save_level(level):
    """Save the level from editor only
    it loads the level JSON file and write the modification"""
    '''Load written level data'''
    level_data = load_json(level.filename)

    '''Modifiy level_data with new value'''
    objects_list = get_element(level_data,"objects")
    if objects_list:

        for i, object_data in enumerate(objects_list):
            object_id = get_element(object_data,"id")
            if object_id is None:
                object_data["id"] = i
    for layer in level.objects:
        for image in layer:
            if image.__class__ is not AnimImage:
                object_id = image.id
                object_data = next((x for x in objects_list if x['id'] == object_id),None)
                if object_data:
                    object_data["pos"] = image.pos.get_list()
                    object_data["angle"] = image.angle
                    object_data["size"] = image.size.get_list()
                else:
                    '''Add GameObject or Image in Level JSON dict'''
                    pass
    write_json(level.filename,level_data)