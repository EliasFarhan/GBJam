'''
Created on 11 sept. 2013

@author: efarhan
'''
import os
from os import listdir
from os.path import isfile,join
from engine.image_manager import img_manager
from engine.const import animation_step
class Image():
    '''Used for The End'''
    def __init__(self,path,pos,size,factor=1):
        self.pos = pos
        self.path = path
        self.size = size
        self.factor = factor

        self.anim_counter = 0
        self.img_index = 0
        self.images = []
        
        self.load_images()
    def load_images(self):
        file_path = 'data/sprites/'+self.path
        files = [ os.path.join(file_path, f) for f in listdir(file_path) if (isfile(join(file_path, f)) and f.find(".png") != -1) ]
        files.sort()
        i = 0
        for img in files:
            self.images.append(img_manager.load_with_size(img, (self.size[0]*self.factor,self.size[1]*self.factor)))
            i+=1
        self.img_number = i
    def loop(self,screen,screen_pos,new_size=1):
        
        if(self.anim_counter == animation_step):
            self.anim_counter = 0
            if(self.img_index == self.img_number-1):
                self.img_index = 0
            else:
                self.img_index += 1
        else:
            self.anim_counter +=1
        img_manager.show(self.images[self.img_index], screen, self.pos, angle=0, rot_func=None, factor=new_size)