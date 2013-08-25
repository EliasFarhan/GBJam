'''
Created on 25 aout 2013

@author: efarhan
'''
import pygame
import os
from os import listdir
from os.path import isfile, join
from engine.image_manager import img_manager


class GameObject():
    def __init__(self):
        self.images = []
    

class Player(GameObject):
    def load_images(self):
        jump_path = 'data/sprites/hero/jump'
        move_path = 'data/sprites/hero/move'
        still_path = 'data/sprites/hero/still'
        self.jump_files = [ os.path.join(jump_path,f) for f in listdir(jump_path) if (isfile(join(jump_path,f)) and f.find(".png") != -1) ]
        self.move_files = [ os.path.join(move_path,f) for f in listdir(move_path) if (isfile(join(move_path,f)) and f.find(".png") != -1) ]
        self.still_files = [ os.path.join(still_path,f) for f in listdir(still_path) if (isfile(join(still_path,f)) and f.find(".png") != -1) ]
        for img in self.jump_files:
            img_manager.load_with_size(img, (64, 64))
        for img in self.move_files:
            img_manager.load_with_size(img, (64, 64))
        for img in self.still_files:
            img_manager.load_with_size(img, (64, 64))
        self.img = self.still_files[0]
    def __init__(self):
        GameObject.__init__(self)
        self.load_images()
        self.joystick = 0
        self.pos = (0, 0)
        if pygame.joystick.get_count() != 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        self.state = 'STILL'
    def loop(self, screen):
        #check events (with joystick)
        
            
        #set animation
        
        #show the current img
        img_manager.show(self.img, screen, screen.get_rect().center)
        
        
if __name__ == '__main__':
    p = Player()
    p.load_images()