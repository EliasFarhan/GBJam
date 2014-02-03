'''
Created on 11 sept. 2013

@author: efarhan
'''

from engine.image_manager import  show_image
from animation.animation import Animation
from engine.init import get_screen_size
from engine.rect import Rect
from game_object.game_object import GameObject

class Image(GameObject):
    '''Can be animated if a directory is given,
    if a png file is given, it will load it
    to load several file, like player do not call this constructor'''
    def __init__(self,path,pos,size=None,angle=0):
        GameObject.__init__(self)
        self.angle = 0
        self.anim = Animation()
        self.size = size
        self.angle = angle
        self.init_image(path,pos)
    def init_image(self,path,pos):
        '''init only one directory or one image,
        for several directories, please set manually
        animation class before'''
        self.pos = pos
        self.anim.path_list = [path]
        self.anim.load_images(self.size)
        if self.size == None:
            self.size = self.anim.size
        self.rect = Rect(self.pos, self.size)
    def loop(self,screen,screen_pos):
        
        self.anim.update_animation()
        pos = self.pos
        try:
            self.screen_relative_pos 
            pos = (pos[0]+self.screen_relative_pos[0]*get_screen_size()[0],
                   pos[1]+self.screen_relative_pos[1]*get_screen_size()[1])
        except AttributeError:
            pass
        show_image(self.anim.img, screen, (pos[0]-screen_pos[0],pos[1]-screen_pos[1]))