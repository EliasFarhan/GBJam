'''
Created on 20 mars 2014

@author: efarhan
'''
from json_export.json_main import get_element
from game_object.game_object_main import GameObject
from game_object.image import Image, AnimImage
from engine.const import path_prefix, log
from game_object.text import Text
from json_export.physic_json import load_physic_objects
from json_export.event_json import load_event
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
        image.update_rect()
        image.angle = angle
    elif image_type == "Image":
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
    else:
        if type(image_type) != unicode:
            return
        for c in image_type:
            if c != '.' and c.isalpha():
                return
        dir_list = image_type.split(".")
        try:
            exec('''from %s import %s'''%(".".join(dir_list[0:len(dir_list)-1]), dir_list[len(dir_list)-1]))
        except ImportError:
            return
        try:
            exec('''image = %s.parse_image(image_data, pos, size, angle)'''%(dir_list[len(dir_list)-1]))
        except Exception as e:
            log('Error with loading image_type: %s'%(image_type)+str(e),1)
            return
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