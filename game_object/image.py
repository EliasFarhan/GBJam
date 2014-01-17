'''
Created on 11 sept. 2013

@author: efarhan
'''
import os
from os import listdir
from os.path import isfile,join
from engine.const import animation_step
from engine.image_manager import load_image_with_size, show_image
from animation.animation import Animation
from engine.init import get_screen_size

class Image():
    '''Can be animated if a directory is given'''
    def __init__(self,path,pos):
        self.anim = Animation()
        self.init_image(path,pos)
    def init_image(self,path,pos):
        self.pos = pos
        self.anim.path_list = [path]
        self.anim.load_images()

    def loop(self,screen,screen_pos):
        
        self.anim.update_animation()
        pos = self.pos
        if self.screen_relative_pos != None:
            pos = (pos[0]+self.screen_relative_pos[0]*get_screen_size()[0],pos[1]+self.screen_relative_pos[1]*get_screen_size()[1])
        show_image(self.anim.img, screen, (pos[0]-screen_pos[0],pos[1]-screen_pos[1]))