'''
Created on 23 oct. 2013

@author: efarhan
'''
import os
from os import listdir
from os.path import isfile, join
class RPGAnimation():
    def __init__(self,img_manager,size):
        self.img_manager = img_manager
        self.img = 0
        self.anim_counter = 0
        self.size = size
    def load_images(self):
        img_path = 'data/sprites/rpg_move'
        
        img_files = [ os.path.join(img_path, f) for f in listdir(img_path) if (isfile(join(img_path, f)) and f.find(".png") != -1) ]
        img_files.sort()

        self.move_img = []
        for img in img_files:
            self.move_img.append(self.img_manager.load_with_size(img, self.size))

        self.img = self.still_img[2]
    def loop(self,state):
        pass