'''
Created on 20 mars 2014

@author: efarhan
'''
from engine.const import log
from json_export.json_main import get_element
from engine.physics import add_dynamic_object, add_static_object, add_static_box
from engine.init import get_screen_size

def load_physic_objects(physics_data,image):
    log(str(physics_data))
    body_type = get_element(physics_data, "type")
    if body_type:
        pos = (0,0)
        if image.pos:
            pos = image.pos
        if image.screen_relative_pos:
            pos = (pos[0]+image.screen_relative_pos[0]*get_screen_size()[0],
                   pos[1]+image.screen_relative_pos[1]*get_screen_size()[1])
        if image.size:
            pos = (pos[0]+image.size[0]/2,pos[1]+image.size[1]/2)
        if body_type == "dynamic":
            image.body = add_dynamic_object(image, pos)
        elif body_type == "static":
            image.body = add_static_object(image,pos)
    pos = (0,0)
    if image.pos:
        pos = image.pos
    if image.screen_relative_pos:
        pos = (pos[0]+image.screen_relative_pos[0]*get_screen_size()[0]+image.size[0]/2,
               pos[1]+image.screen_relative_pos[1]*get_screen_size()[1]+image.size[1]/2)
    if not image.body:
        image.body = add_static_object(image,pos)
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
                    size = (image.size[0]/2,image.size[1]/2)
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