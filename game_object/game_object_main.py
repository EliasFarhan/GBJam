"""
Created on Feb 3, 2014

@author: efarhan
"""
import math
from engine.rect import Rect
from engine.const import log, CONST
from engine.image_manager import draw_rect
from engine.physics import show_fixtures, get_body_position, set_body_position
from engine.init import get_screen_size
from engine.vector import Vector2



class GameObject:
    def __init__(self):
        self.id = ""
        self.angle = 0
        self.screen_relative = False
        self.screen_relative_pos = None
        self.body = None
        self.screen_factor = 1
        self.img_loop = False
        self.fixtures = []
        self.pos = Vector2()
        self.not_rot_pos = Vector2()
        self.size = Vector2()
        self.rect = None
        self.click_rect = None
        self.remove = False
        self.event = None

    def scale(self, x, y):

        self.size = self.size*Vector2(x*CONST.scale_speed+1,
                                      y*CONST.scale_speed+1)
        self.update_rect()
    
    def update_rect(self):
        pos = Vector2()
        if self.pos:
            pos = self.pos
        if self.screen_relative_pos:
            pos = pos+self.screen_relative_pos*get_screen_size()
        self.rect = Rect(pos, self.size, self.angle)

        center_pos = Vector2()
        if self.body:
            center_pos = get_body_position(self.body)
            if self.screen_relative_pos:
                center_pos = center_pos - self.screen_relative_pos*get_screen_size()

            self.not_rot_pos = center_pos - self.size/2

        v = self.size/2
        v.rotate(-self.angle)
        if self.angle > 0:
            pos = self.not_rot_pos + (v-self.size/2)
        else:
            pos = self.not_rot_pos + (self.size/2-v)

        v = Vector2(self.size.x,0)
        v.rotate(self.angle)
        v = Vector2(self.size.x,self.size.y+math.fabs(v.y))
        self.click_rect = Rect(pos,v)

    def move(self, delta):
        self.pos = self.pos+delta
        if self.body:
            body_pos = get_body_position(self.body)
            set_body_position(self.body,body_pos+delta)
        self.update_rect()

    def set_pos(self,init_pos,delta_pos):
        delta_move = delta_pos-(self.pos-init_pos)
        self.move(delta_move)

    def set_angle(self, angle, center=True):
        pos = Vector2()

        self.angle = angle % 360
        if self.angle > 180:
            self.angle -= 360

        if self.body:
            self.body.angle = self.angle*math.pi/180
        if center:
            if self.body:
                pos = get_body_position(self.body)
                if self.screen_relative_pos:
                    pos = pos - self.screen_relative_pos*get_screen_size()
                self.not_rot_pos = pos - self.size/2
                v = self.size/2
                v.rotate(self.angle)
                self.pos = self.not_rot_pos - v + self.size/2
        else:
            '''TODO: Readjust body pos'''
            pass

        self.update_rect()
        
    def check_click(self,mouse_pos,screen_pos):
        if CONST.debug:
            log("Check Click:{0} {1}".format(str(screen_pos.get_tuple()), str(mouse_pos.get_tuple())))
        point_pos = screen_pos + mouse_pos
        if self.click_rect:
            return self.click_rect.collide_point(point_pos)
        elif self.rect:
            return self.click_rect.collide_point(point_pos)
        else:
            return False

    def execute_event(self):
        if self.event:
            self.event.execute()

    def loop(self,screen,screen_pos):
        pos = (0,0)
        if self.pos:
            pos = self.pos
        
        if self.screen_relative_pos is not None:
            pos = pos+self.screen_relative_pos*get_screen_size()
        
        if self.screen_relative:
            pos = self.pos
        else:
            pos = pos-screen_pos
        if CONST.debug:
            self.update_rect()
            draw_rect(screen, screen_pos, self.rect, (0,0,255,200), self.angle)
            if self.click_rect:
                draw_rect(screen,screen_pos,self.click_rect,(0,255,0,100))
            if self.body:
                show_fixtures(screen, screen_pos, self.body)

    def set_position(self,pos):
        if self.screen_relative_pos:
            self.pos = (pos[0]-self.screen_relative_pos[0],pos[1]-self.screen_relative_pos[1])
        else:
            self.pos = pos

    @staticmethod
    def generate_json(json_dict, game_object, layer):
        json_dict["layer"] = layer
        json_dict["angle"] = game_object.angle
        json_dict["pos"] = game_object.pos
        """
        TODO: Generate JSON from physics objects

        "physic_objects": {
                "fixtures": [
                    {
                        "type": "box",
                        "user_data": 11
                    }
                ],
                "type": "static"
            },"""
        from game_object.image import Image
        if game_object.__class__ == GameObject:
            json_dict["type"] = "GameObject"
        elif game_object.__class__ == Image:
            json_dict["type"] = "Image"
        json_dict["id"] = game_object.id
        json_dict["size"] = game_object.size
