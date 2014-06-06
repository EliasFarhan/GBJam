"""
Created on Feb 3, 2014

@author: efarhan
"""
import math
from engine.rect import Rect
from engine.const import log, CONST
from engine.img_manager import img_manager
from engine.physics_manager import physics_manager, BodyType
from engine.init import engine
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
        """update body"""
        if self.body:
            physics_manager.remove_body(self.body)
            self.body = physics_manager.add_body(self.not_rot_pos, BodyType.static)
            physics_manager.add_box(self.body,Vector2(),self.size/2)
        self.update_rect()
    
    def update_rect(self):
        pos = Vector2()
        if self.pos:
            pos = self.pos
        if self.screen_relative_pos:
            pos = pos+self.screen_relative_pos*engine.get_screen_size()
        self.rect = Rect(pos, self.size, self.angle)

        center_pos = Vector2()
        if self.body:
            center_pos = physics_manager.get_body_posdition(self.body)
            if self.screen_relative_pos:
                center_pos = center_pos - self.screen_relative_pos*engine.get_screen_size()

            self.not_rot_pos = center_pos

        v = self.size/2
        v.rotate(-self.angle)
        if self.angle > 0:
            pos = self.not_rot_pos + (v-self.size/2)
        else:
            pos = self.not_rot_pos + (self.size/2-v)

        size_y = Vector2(self.size.x, 0)
        size_y.rotate(self.angle)
        v = Vector2(self.size.x, self.size.y + math.fabs(size_y.y))
        self.click_rect = Rect(self.not_rot_pos-v/2, v)

    def move(self, delta):
        self.pos = self.pos+delta
        if self.body:
            body_pos = physics_manager.get_body_position(self.body)
            physics_manager.set_body_position(self.body,body_pos+delta)
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
                pos = physics_manager.get_body_position(self.body)
                if self.screen_relative_pos:
                    pos = pos - self.screen_relative_pos*physics_manager.get_screen_size()
                self.not_rot_pos = pos - self.size/2
                v = self.size/2
                v.rotate(self.angle)
                self.pos = self.not_rot_pos - v + self.size/2
        else:
            '''TODO: Readjust body pos'''
            pass

        self.update_rect()
        
    def check_click(self, mouse_pos, screen_pos):
        if CONST.debug:
            from game_object.text import Text
            if isinstance(self, Text):
                log("Check click for text: "+self.text)
        if not self.screen_relative:
            point_pos = screen_pos + mouse_pos
        else:
            point_pos = mouse_pos
        if self.click_rect and not self.screen_relative:
            return self.click_rect.collide_point(point_pos)
        elif self.rect:
            return self.rect.collide_point(point_pos)
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
            pos = pos + self.screen_relative_pos*engine.get_screen_size()
        
        if self.screen_relative:
            pos = self.pos
        else:
            pos = pos-screen_pos
        if CONST.debug:
            self.update_rect()
            if not self.screen_relative:
                img_manager.draw_rect(screen, screen_pos, self.rect, (0,0,255,200), self.angle)
                if self.click_rect:
                    img_manager.draw_rect(screen,screen_pos,self.click_rect,(0,255,0,100))

    def set_position(self,pos):
        if self.screen_relative_pos:
            self.pos = (pos[0]-self.screen_relative_pos[0],pos[1]-self.screen_relative_pos[1])
        else:
            self.pos = pos

