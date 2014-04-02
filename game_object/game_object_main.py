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
        self.pos = None
        self.not_rot_pos = None
        self.size = None
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
        self.rect = Rect(pos, self.size,self.angle)

        center_pos = Vector2()
        if self.body:
            center_pos = get_body_position(self.body)
            if self.screen_relative_pos:
                center_pos = center_pos - self.screen_relative_pos*get_screen_size()

        not_rot_pos = center_pos - self.size/2

        v = self.size/2
        v.rotate(-self.angle)
        if self.angle > 0:
            pos = not_rot_pos + (v-self.size/2)
        else:
            pos = not_rot_pos + (self.size/2-v)

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
        
    def rotate(self,right):
        self.angle += right
        self.update_rect()

    def set_pos(self,init_pos,delta_pos):
        delta_move = delta_pos-(self.pos-init_pos)
        self.move(delta_move)

    def set_angle(self, angle):
        pos = Vector2()
        if self.body:
            pos = get_body_position(self.body)
            if self.screen_relative_pos:
                pos = pos - self.screen_relative_pos*get_screen_size()

        v = self.size/2
        v.rotate(-self.angle)
        self.not_rot_pos = pos - self.size/2
        self.angle = angle

        if self.body:
            self.body.angle = self.angle*math.pi/180
        v = self.size/2
        v.rotate(self.angle)
        self.pos = self.not_rot_pos + self.size/2 + (v-self.size/2)
        self.update_rect()
        
    def check_click(self,mouse_pos,screen_pos):
        if CONST.debug:
            log("Check Click:{0} {1}".format(str(screen_pos.get_tuple()), str(mouse_pos.get_tuple())))
        point_pos = screen_pos + mouse_pos

        return self.click_rect.collide_point(point_pos)

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
