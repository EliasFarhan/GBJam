'''
Created on 20 mars 2014

@author: efarhan
'''
from json_export.json_main import get_element
from game_object.game_object_main import GameObject
from game_object.image import Image
from engine.const import CONST,log
from game_object.text import Text
from json_export.physic_json import load_physic_objects
from json_export.event_json import load_event
from engine.vector import Vector2


global_object_id = 0


def reset_object_id():
    global global_object_id
    global_object_id = 0


def get_last_object_id():
    global global_object_id
    return global_object_id


def set_last_object_id(new_id):
    global global_object_id
    global_object_id = new_id


def load_image_from_json(image_data, level, image_type=None):
    global global_object_id
    image = None
    if image_type is None:
        try:
            image_type = image_data["type"]
        except KeyError:
            log("Error: No image_type for:" + str(image_data),1)
            return 
    pos = get_element(image_data, "pos")
    size = get_element(image_data, "size")
    layer = get_element(image_data, "layer")
    angle = get_element(image_data, "angle")
    object_id = get_element(image_data, "id")
    if object_id is None:
        object_id = global_object_id
    if angle is None:
        angle = 0
    if image_type == "GameObject":
        image = GameObject()
        image.pos = Vector2(pos)
        image.size = Vector2(size)
        image.update_rect()
        image.angle = angle
        image.id = object_id
    elif image_type == "Image":
        image = Image.parse_image(image_data, pos, size, angle)
        if image is not None:
            image.id = object_id
    elif image_type == "Text":
        font = get_element(image_data, "font")
        text = get_element(image_data, "text")
        color = get_element(image_data, "color")
        if font and text:
            font = CONST.path_prefix+font
        else:
            log("Invalid arg font and text not defined for Text",1)
            return
        if not color:
            color = [0,0,0]
        image = Text(pos, size, font, text, angle,color)
        image.id = object_id
    else:
        if not isinstance(image_type,CONST.string_type):
            log("image_type not a string",1)
            return
        for c in image_type:
            if c != '.' and c != '_' and not c.isalpha():
                return
        dir_list = image_type.split(".")
        try:
            exec('''from %s import %s'''%(".".join(dir_list[0:len(dir_list)-1]), dir_list[len(dir_list)-1]))
        except ImportError:
            log("Error: ImportError with: "+str(image_type),1)
            return
        try:
            d = locals()
            exec('''image = %s.parse_image(image_data, pos, size, angle)'''%(dir_list[len(dir_list)-1]),globals(),d)
            image = d['image']
        except Exception as e:
            log('Error with loading image_type: %s'%(image_type)+str(e),1)
            return
    physic_objects = get_element(image_data, "physic_objects")
    if physic_objects:
        load_physic_objects(physic_objects, image)
    
    event_path = get_element(image_data, "event")
    if image and event_path:
        image.event = load_event(event_path)
    if not layer or layer < 0:
        layer = 1
    elif layer > len(level.objects)-1:
        layer = len(level.objects)-1
    if image:
        level.objects[layer-1].append(image)
    global_object_id += 1
    return image