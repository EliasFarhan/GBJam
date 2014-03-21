'''
Created on Feb 3, 2014

@author: efarhan
'''
from engine.rect import Rect
from engine.const import log, debug
from engine.image_manager import draw_rect
from engine.physics import show_fixtures
from engine.init import get_screen_size
from engine.vector import Vector2

class GameObject:
    def __init__(self):
        self.angle = 0
        self.screen_relative = False
        self.screen_relative_pos = None
        self.body = None
        self.screen_factor = 1
        self.img_loop = False
        self.fixtures = []
        self.pos = None
        self.size = None
        self.rect = None
        self.remove = False
        self.event = None
    def scale(self,enlargement,speed=1.1):
        scale_speed = speed
        if not enlargement:
            scale_speed = 1/speed
        self.size = self.size*scale_speed
        self.update_rect()
    
    def update_rect(self):
        pos = Vector2()
        if self.pos:
            pos = self.pos
        if self.screen_relative_pos:
            pos = pos+self.screen_relative_pos*get_screen_size()
        self.rect = Rect(pos, self.size,self.angle)
        
    def move(self,horizontal=0,vertical=0):
        self.pos = self.pos+Vector2().coordinate(horizontal,vertical)
        self.update_rect()
        
    def rotate(self,right):
        self.angle += right
        self.update_rect()
        
    def set_angle(self,angle):
        self.angle = angle
        self.update_rect()
        
    def check_click(self,mouse_pos,screen_pos):
        log(str(screen_pos)+" "+str(mouse_pos))
        point_pos = (screen_pos[0]+mouse_pos[0], screen_pos[1]+mouse_pos[1])
        return self.rect.collide_point(point_pos)
    def execute_event(self):
        if self.event:
            self.event.execute()
    def loop(self,screen,screen_pos):
        pos = (0,0)
        if self.pos:
            pos = self.pos
        
        if self.screen_relative_pos != None: 
            pos = pos+self.screen_relative_pos*get_screen_size()
        
        if self.screen_relative:
            pos = self.pos
        else:
            pos = pos-screen_pos
        if debug:
            self.update_rect()
            draw_rect(screen, screen_pos, self.rect, (0,0,255,200), self.angle)
            if self.body:
                show_fixtures(screen, screen_pos, self.body)
    def set_position(self,pos):
        if self.screen_relative_pos:
            self.pos = (pos[0]-self.screen_relative_pos[0],pos[1]-self.screen_relative_pos[1])
        else:
            self.pos = pos
