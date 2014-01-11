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

class Image():
    '''Can be animated if a directory is given'''
    def __init__(self,path,pos):
        self.pos = pos
        self.anim = Animation()
        self.anim.path_list = [path]
        self.anim.load_images()

    def loop(self,screen,screen_pos):
        
        self.anim.update_animation()
        show_image(self.anim.img, screen, (self.pos[0]-screen_pos[0],self.pos[1]-screen_pos[1]))