'''
Created on 11 janv. 2014

@author: efarhan
'''
import json

from engine.const import log,path_prefix
from game_object.image import Image, AnimImage
from json_export.json_main import load_json, get_element
from json_export.event_json import load_event
from game_object.text import Text
from game_object.game_object_main import GameObject
from engine.physics import add_dynamic_object, add_static_box, add_static_object

def load_image_from_json(image_data,level,image_type=None):
    image = None
    if image_type == None:
        try:
            image_type = image_data["type"]
        except KeyError:
            return 
    pos = get_element(image_data, "pos")
    size = get_element(image_data, "size")
    layer = get_element(image_data, "layer")
    angle = get_element(image_data, "angle")
    if angle == None:
        angle = 0
    if image_type == "GameObject":
        image = GameObject()
        image.pos = pos
        image.size = size
        image.angle = angle
    if image_type == "Image":
        image = Image.parse_image(image_data, pos, size, angle)
    elif image_type == "AnimImage":
        image = AnimImage.parse_image(image_data, pos, size, angle)
    elif image_type == "Text":
        font = get_element(image_data, "font")
        text = get_element(image_data, "text")
        color = get_element(image_data, "color")
        if font and text:
            font = path_prefix+font
        else:
            log("Invalid arg font and text not defined for Text",1)
            return
        if not color:
            color = [0,0,0]
        image = Text(pos, size, font, text, angle,color)
    
    physic_objects = get_element(image_data, "physic_objects")
    if physic_objects:
        load_physic_objects(physic_objects,image)
    
    event_path = get_element(image_data, "event")
    if event_path:
        image.event = load_event(event_path)
    if not layer:
        layer = 1
    elif layer > len(level.images)-1:
        layer = len(level.images)-1
    if image:
        level.images[layer-1].append(image)
    return image

def load_physic_objects(physics_data,image):
    log(str(physics_data))
    body_type = get_element(physics_data, "type")
    if body_type:
        if body_type == "dynamic":
            image.body = add_dynamic_object(image, image.pos)
        elif body_type == "static":
            image.body = add_static_object(image,image.pos)
    if not image.body:
        image.body = add_static_object(image,image.pos)
    fixtures_data = get_element(physics_data,"fixtures")
    if fixtures_data:
        for physic_object in fixtures_data:
            obj_type = get_element(physic_object, "type")
            if obj_type == "box":
                pos = get_element(physic_object,"pos")
                if not pos:
                    pos = (0,0)
                size = get_element(physic_object,"size")
                if not size:
                    size = image.size
                sensor = get_element(physic_object, "sensor")
                if sensor == None:
                    sensor = False
                user_data = get_element(physic_object,"user_data")
                if user_data == None:
                    user_data = image
                angle = get_element(physic_object,"angle")
                if angle == None:
                    angle = 0
                image.fixtures.append(add_static_box(image.body, pos, size, angle, user_data, sensor))
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
        player_data = get_element(level_data, 'player')
        if player_data:
            '''load the json containing the player
            and treat it as an AnimImage'''
            player = None
            if type(player_data) == unicode:
                player_json = load_json(path_prefix+player_data)
                player = load_image_from_json(player_json, level, "AnimImage")
            elif type(player_data) == dict:
                player = load_image_from_json(player_data, level, "AnimImage")
            
            if player:
                level.player = player
        bg_color = get_element(level_data,'bg_color')
        if bg_color != None:
            level.bg_color = bg_color
        show_mouse = get_element(level_data,'show_mouse')
        if show_mouse != None:
            level.show_mouse = show_mouse
        
        use_physics = get_element(level_data,'use_physics')
        if use_physics != None:
            level.use_physics = use_physics
        network = get_element(level_data, 'network')
        if network != None:
            level.use_network = network
        
        event_data = get_element(level_data, "event")
        if event_data:
            for e in event_data.keys():
                level.event[e] = load_event(event_data[e])

        images_dict = get_element(level_data, 'images')
        if images_dict != None:
            for image_data in level_data['images']:
                if type(image_data) == unicode:
                    load_image_from_json(load_json(image_data), level, None)
                
                elif type(image_data) == dict:
                    image_type = get_element(image_data,"type")
                    load_image_from_json(image_data,level,image_type)
        return True
    return False
'''def save_level(level):
    
    
    level_data = {}
    level_data['player'] = level.player.filename
    level_data['background_color'] = level.bg_color
    level_data['physic_objects'] = []
    for physic_object in level.physic_objects:
        if physic_object.__class__ == PhysicRect:
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
    file.close()'''