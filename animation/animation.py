'''
Created on 11 dec. 2013

@author: efarhan
'''
import os
from os import listdir
from os.path import isfile, join
from engine.image_manager import img_manager
class Animation():
    def __init__(self,player,size):
        self.player = player
        self.img = 0
        self.size = size
        self.path = ""
        self.state = ""
    def load_images(self):
        
        files = [ os.path.join(self.path, f) for f in listdir(self.path) if (isfile(join(self.path, f)) and f.find(".png") != -1) ]
        files.sort()
        self.img_indexes = []
        for f in files:
            self.img_indexes.append(img_manager.load_with_size(f, self.size))
        self.img = self.img_indexes[0]
    def loop(self):
        pass
    def init_physics(self):
        pass
    def set_state(self,state):
        self.state = state