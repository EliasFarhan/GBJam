'''
Created on 25 aout 2013

@author: efarhan
'''
import pygame
import os
from os import listdir
from os.path import isfile, join
from engine.image_manager import img_manager
from pygame.locals import *

class GameObject():
    def __init__(self):
        self.images = []
    

class Player(GameObject):
    def load_images(self):
        jump_path = 'data/sprites/hero/jump'
        move_path = 'data/sprites/hero/move'
        still_path = 'data/sprites/hero/still'
        self.jump_files = [ os.path.join(jump_path, f) for f in listdir(jump_path) if (isfile(join(jump_path, f)) and f.find(".png") != -1) ]
        self.move_files = [ os.path.join(move_path, f) for f in listdir(move_path) if (isfile(join(move_path, f)) and f.find(".png") != -1) ]
        self.still_files = [ os.path.join(still_path, f) for f in listdir(still_path) if (isfile(join(still_path, f)) and f.find(".png") != -1) ]
        for img in self.jump_files:
            img_manager.load_with_size(img, (64, 64))
        for img in self.move_files:
            img_manager.load_with_size(img, (64, 64))
        for img in self.still_files:
            img_manager.load_with_size(img, (64, 64))
        self.img = self.still_files[1]
    def __init__(self):
        GameObject.__init__(self)
        self.load_images()
        self.joystick = 0
        self.pos = (0, 0)
        self.UP, self.RIGHT = 0, 0
        self.anim_counter = 0
        if pygame.joystick.get_count() != 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        self.state = 'STILL'
    def loop(self, screen):
        # check events (with joystick)
        for event in pygame.event.get(): 
            if (self.joystick != 0 and event.type == JOYHATMOTION):
                if (self.joystick.get_hat(0) == (0, 1)):
                    self.UP = 1
                elif(self.joystick.get_hat(0) == (0, -1)):
                    # DOWN
                    pass
                elif(self.joystick.get_hat(0) == (1, 0)):
                    self.RIGHT = 1
                elif(self.joystick.get_hat(0) == (-1, 0)):
                    # LEFT
                    pass
                elif(self.joystick.get_hat(0) == (0, 0)):
                    self.UP, self.RIGHT = 0, 0
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.UP = 1
                elif event.key == K_DOWN:
                    # DOWN
                    pass
                elif event.key == K_RIGHT:
                    self.RIGHT = 1
                elif event.key == K_LEFT:
                    # LEFT
                    pass
            if event.type == KEYUP:
                if event.key == K_UP:
                    self.UP = 0
                elif event.key == K_DOWN:
                    # DOWN
                    pass
                elif event.key == K_RIGHT:
                    self.RIGHT = 0
                elif event.key == K_LEFT:
                    # LEFT
                    pass
                elif event.key == K_ESCAPE:
                    from engine.loop import end as end
                    end()
                        
            if event.type == QUIT:
                from engine.loop import end as end
                end()
                    
                        
        # set animation
        if self.UP:
            self.img = self.jump_files[1]
        
        elif self.RIGHT:
            img_move = [0, 2, 5]
            a = self.img == self.move_files[img_move[0]]
            b = self.img == self.move_files[img_move[1]]
            c = self.img == self.move_files[img_move[2]]
            d = a or b or c
            time = (self.anim_counter > 2)
            if not d:
                self.img = self.move_files[img_move[0]]
            else:
                if time:
                    if a:
                        self.img = self.move_files[img_move[1]]
                    elif b:
                        self.img = self.move_files[img_move[2]]
                    elif c:
                        self.img = self.move_files[img_move[0]]
                    self.anim_counter = 0
                else:
                    self.anim_counter += 1
                
        else:
            self.img = self.still_files[1]
        # show the current img
        img_manager.show(self.img, screen, screen.get_rect().center)
        
        
if __name__ == '__main__':
    p = Player()
    p.load_images()
