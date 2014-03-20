'''
Created on Feb 3, 2014

@author: efarhan
'''
from engine.rect import Rect
from engine.const import log, debug
from engine.image_manager import draw_rect
from engine.physics import show_fixtures
from engine.init import get_screen_size

class GameObject:
    def __init__(self):
        self.angle = 0
        self.screen_relative = False
        self.screen_relative_pos = None
        self.body = None
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
        self.size = (int(self.size[0]*scale_speed),int(self.size[1]*scale_speed))
        self.update_rect()
    
    def update_rect(self):
        self.rect = Rect(self.pos, self.size)
        
    def move(self,horizontal=0,vertical=0):
        self.pos = (self.pos[0]+horizontal,self.pos[1]+vertical)
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
            pos = (pos[0]+self.screen_relative_pos[0]*get_screen_size()[0],
                   pos[1]+self.screen_relative_pos[1]*get_screen_size()[1])
        
        if self.screen_relative:
            pos = self.pos
        else:
            pos = (pos[0]-screen_pos[0],pos[1]-screen_pos[1])
        if debug:
            self.update_rect()
            #draw_rect(screen, screen_pos, self.rect, (0,0,255,200), self.angle)
            if self.body:
                show_fixtures(screen, screen_pos, self.body)
            
