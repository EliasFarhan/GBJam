'''
Created on 11 dec. 2013

@author: efarhan
'''
import os
from os import listdir
from os.path import isfile, join
from engine.image_manager import load_image
from engine.const import animation_step

class Animation():
    def __init__(self):
        self.img = 0
        self.path = ""
        self.state_range = {}
        self.path_list = []
        self.state = ""
        self.anim_counter = 0
        self.anim_speed = animation_step
    def load_images(self):
        self.img_indexes = []
        
        for p in self.path_list:
            
            path = self.path+p
            files = []
            if ".png" in path:
                files = [path]
            else:
                files = [ os.path.join(path, f) for f in listdir(path) if (isfile(join(path, f)) and f.find(".png") != -1) ]
            files.sort()
            for f in files:
                self.img_indexes.append(load_image(f))
            self.img = self.img_indexes[0]
        
    def update_animation(self,state="",invert=False):
        self.state = state
        if(self.anim_counter == self.anim_speed):
            anim_index = []
            if self.state_range == {}:
                anim_index = self.img_indexes
            else:
                try:
                    anim_index = self.img_indexes[self.state_range[state][0]:self.state_range[state][1]]
                except KeyError:
                    return
            try:
                find_index = anim_index.index(self.img)
                if not invert:
                    if find_index == len(anim_index)-1:
                        self.img = anim_index[0]
                    else:
                        self.img = anim_index[find_index+1]
                else:
                    if find_index == 0:
                        self.img = anim_index[len(anim_index)-1]
                    else:
                        self.img = anim_index[find_index-1]
            except ValueError:
                self.img = anim_index[0]
            self.anim_counter = 0
        else:
            self.anim_counter += 1