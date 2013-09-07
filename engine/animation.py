'''
Created on Sep 5, 2013

@author: efarhan
'''
import os
from os import listdir
from os.path import isfile, join
class DemoAnimation():
    '''Manage the images and the animation of the demo-player'''
    def __init__(self, img_manager,size):
        self.img_manager = img_manager
        self.img = 0
        self.anim_counter = 0
        self.size = size
    def load_images(self):
        jump_path = 'data/sprites/hero/jump'
        move_path = 'data/sprites/hero/move'
        still_path = 'data/sprites/hero/still'
        
        jump_files = [ os.path.join(jump_path, f) for f in listdir(jump_path) if (isfile(join(jump_path, f)) and f.find(".png") != -1) ]
        jump_files.sort()
        move_files = [ os.path.join(move_path, f) for f in listdir(move_path) if (isfile(join(move_path, f)) and f.find(".png") != -1) ]
        move_files.sort()
        still_files = [ os.path.join(still_path, f) for f in listdir(still_path) if (isfile(join(still_path, f)) and f.find(".png") != -1) ]
        still_files.sort()
        
        self.jump_img = []
        self.move_img = []
        self.still_img = []
        for img in jump_files:
            self.jump_img.append(self.img_manager.load_with_size(img, self.size))
        for img in move_files:
            self.move_img.append(self.img_manager.load_with_size(img, self.size))
        for img in still_files:
            self.still_img.append(self.img_manager.load_with_size(img, self.size))
        self.img = self.still_img[0]
    def loop(self,state):
        if(state == 'jump'):
            self.img = self.jump_img[0]
        elif(state == 'move_right'):
            if(self.anim_counter == 3):
                anim_index = [self.move_img[0],self.move_img[2],self.move_img[4]]
                try:
                    find_index = anim_index.index(self.img)
                    if find_index == len(anim_index)-1:
                        self.img = anim_index[0]
                    else:
                        self.img = anim_index[find_index+1]
                except ValueError:
                    self.img = anim_index[0]
                self.anim_counter = 0
            else:
                self.anim_counter += 1
        elif(state == 'move_left'):
            if(self.anim_counter == 3):
                anim_index = [self.move_img[1],self.move_img[3],self.move_img[5]]
                try:
                    find_index = anim_index.index(self.img)
                    if find_index == len(anim_index)-1:
                        self.img = anim_index[0]
                    else:
                        self.img = anim_index[find_index+1]
                except ValueError:
                    self.img = anim_index[0]
                self.anim_counter = 0
            else:
                self.anim_counter += 1
        elif(state == 'still'):
            self.img = self.still_img[0]