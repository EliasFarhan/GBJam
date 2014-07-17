'''
Created on 20 mars 2014

@author: efarhan
'''
import math

from engine.const import CONST
from json_export.json_main import get_element
from physics_engine.physics_manager import BodyType, pixel2meter
from engine.init import engine
from engine.vector import Vector2
from physics_engine.physics_manager import physics_manager


def load_physic_objects(physics_data,image):
    if image is None:
        return
    body_type = get_element(physics_data, "type")
    if body_type:
        pos = Vector2()
        if image.pos:
            pos = image.pos
        if image.screen_relative_pos:
            pos = pos+image.screen_relative_pos*engine.get_screen_size()
        if image.size:
            pos = pos+image.size/2
        if body_type == "dynamic":
            image.body = physics_manager.add_body(pos, BodyType.dynamic)
        elif body_type == "static":
            image.body = physics_manager.add_body(pos, BodyType.static)
        elif body_type == 'kinematic':
            image.body = physics_manager.add_body(pos, BodyType.kinematic)
    pos = (0,0)
    if image.pos:
        pos = image.pos
    if image.screen_relative_pos:
        pos = pos+image.screen_relative_pos*engine.get_screen_size()+image.size/2
    angle = get_element(physics_data, "angle")
    if angle:
        image.body.angle = angle*math.pi/180
    else:
        if image.body and image.angle != 0:
            if CONST.physics == 'b2':
                image.body.angle = image.angle*math.pi/180
            elif CONST.physics == 'pookoo':
                #TODO: set angle for body
                pass
            '''Set new pos for body'''
            v = image.size/2
            v.rotate(image.angle)
            pos = image.pos+v
            pos = pixel2meter(pos)
            if CONST.physics == 'b2':
                image.body.position = pos.get_tuple()
            elif CONST.physics == 'pookoo':
                #TODO: set pos for body
                pass
            
    fixtures_data = get_element(physics_data,"fixtures")
    if fixtures_data:
        for physic_object in fixtures_data:
            sensor = get_element(physic_object, "sensor")
            if sensor is None:
                sensor = False
            user_data = get_element(physic_object,"user_data")
            if user_data is None:
                user_data = image
            obj_type = get_element(physic_object, "type")
            if obj_type == "box":
                pos = get_element(physic_object,"pos")
                if not pos:
                    pos = Vector2()

                size = get_element(physic_object,"size")
                if not size:
                    size = image.size/2

                angle = get_element(physic_object,"angle")
                if angle is None:
                    
                    angle = 0
                image.fixtures.append(physics_manager.add_box(image.body, Vector2(pos), Vector2(size), angle, user_data, sensor))
            elif obj_type == "circle":
                pos = get_element(physic_object,"pos")
                if not pos:
                    pos = (0,0)
                radius = get_element(physic_object,"radius")
                if not radius:
                    radius = 1

                image.fixtures.append(physics_manager.add_circle(image.body,pos,radius,sensor,user_data))
