"""
Created on 11 janv. 2014

@author: efarhan
"""
import json
from numbers import Number

from engine.const import log,CONST
from game_object.game_object_main import GameObject
from game_object.image import Image
from json_export.json_main import load_json, get_element, write_json
from json_export.event_json import load_event
from json_export.image_json import load_image_from_json, reset_object_id, get_last_object_id, set_last_object_id
from levels.gui import GUI


def load_level(level):
    """
    Import a level with:

    -Physics static object
    -Images with or without animation
    -IA (if any)
    -Player position, size, etc... but not recreate the player!!!
    """
    level_data = load_json(CONST.path_prefix+level.filename)
    if level_data is not None:
        log("LOAD PLAYER")
        player_data = get_element(level_data, 'player')
        if player_data is not None:
            '''load the json containing the player
            and treat it as an AnimImage'''
            player = None
            if isinstance(player_data, CONST.string_type):
                log("Loading player "+player_data)
                player_json = load_json(CONST.path_prefix + player_data)
                player = load_image_from_json(player_json, level)

            elif isinstance(player_data,dict):
                player = load_image_from_json(player_data, level)
            else:
                log("Warning: Invalid format for player JSON",1)
            if player:
                level.player = player
        log("LOAD GUI")
        gui_data = get_element(level_data, 'gui')
        if gui_data is not None:
            '''load the json containing the gui
            parameters'''
            if isinstance(gui_data, CONST.string_type):
                GUI.load_gui_json(load_json(gui_data),level)
            elif isinstance(gui_data,dict):
                GUI.load_gui_json(gui_data,level)
            else:
                log("Warning: invalid format for GUI JSON",1)
        log("LOAD_BG COLOR")
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
        log("LOAD EVENTS")
        event_data = get_element(level_data, "events")
        if event_data:
            for e in event_data.keys():
                level.event[e] = load_event(event_data[e])

        log("LOAD ImAGE OBJECTS")
        objects_dict = get_element(level_data, 'objects')
        reset_object_id()
        if objects_dict is not None:
            for object_data in objects_dict:
                if isinstance(object_data, CONST.string_type):
                    load_image_from_json(load_json(object_data), level, None)
                
                elif isinstance(object_data,dict):
                    image_type = get_element(object_data,"type")
                    load_image_from_json(object_data,level,image_type)
        log("END OF LOADING")
        return True
    return False


def save_level(level):
    """Save the level from editor only
    it loads the level JSON file and write the modification"""
    '''Load written level data'''
    level_data = load_json(level.filename)
    objects_list = get_element(level_data, "objects")
    for layer_index, layer in enumerate(level.objects):
        for image in layer:
            if isinstance(image,GameObject):
                object_id = image.id
                object_data = next((x for x in objects_list if x['id'] == object_id), None)
                if not object_data:
                    '''Add GameObject or Image in Level JSON dict'''
                    object_id = get_last_object_id()
                    set_last_object_id(object_id+1)
                    object_data = {"id": object_id}
                    objects_list.append(object_data)
                    if isinstance(image,GameObject):
                        object_data["type"] = "GameObject"
                    elif isinstance(image, Image):
                        object_data["type"] = "Image"
                        object_data["path"] = image.path
                object_data["pos"] = image.pos.get_list()
                object_data["angle"] = image.angle
                object_data["size"] = image.size.get_list()
                object_data["layer"] = layer_index + 1
                if image.body and not get_element(object_data, "physic_objects"):
                    """Add physic description

                    TODO:
                    -circle shape
                    -none middle pos for fixtures"""
                    physic_objects = {}
                    if CONST.render == 'sfml':
                        import Box2D as b2
                        if image.body.type == b2.b2_staticBody:
                            physic_objects["type"] = "static"
                        elif image.body.type == b2.b2_kinematicBody:
                            physic_objects["type"] = "kinematic"
                        elif image.body.type == b2.b2_dynamicBody:
                            physic_objects["type"] = "dynamic"
                        body_fixtures = []
                        for fixture in image.body.fixtures:
                            fixture_data = {}
                            if isinstance(fixture.userData, Number):
                                fixture_data["user_data"] = fixture.userData
                            if isinstance(fixture.shape,b2.b2PolygonShape):
                                fixture_data["type"] = "box"

                            body_fixtures.append(fixture_data)
                        physic_objects["fixtures"] = body_fixtures
                    object_data["physic_objects"] = physic_objects

    log(objects_list)
    write_json(level.filename,level_data)