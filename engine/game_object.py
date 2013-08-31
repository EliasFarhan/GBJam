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
import engine.level_manager


class GameObject():
    def __init__(self):
        self.img_manager = img_manager
        self.pos = (0, 0)
        self.size = (0, 0)
    def loop(self,screen):
        pass
    

class Player(GameObject):
    def load_images(self):
        jump_path = 'data/sprites/hero/jump'
        move_path = 'data/sprites/hero/move'
        still_path = 'data/sprites/hero/still'
        self.jump_files = [ os.path.join(jump_path, f) for f in listdir(jump_path) if (isfile(join(jump_path, f)) and f.find(".png") != -1) ]
        self.move_files = [ os.path.join(move_path, f) for f in listdir(move_path) if (isfile(join(move_path, f)) and f.find(".png") != -1) ]
        self.still_files = [ os.path.join(still_path, f) for f in listdir(still_path) if (isfile(join(still_path, f)) and f.find(".png") != -1) ]
        for img in self.jump_files:
            self.img_manager.load_with_size(img, self.size)
        for img in self.move_files:
            self.img_manager.load_with_size(img, self.size)
        for img in self.still_files:
            self.img_manager.load_with_size(img, self.size)
        self.img = self.still_files[1]
    def __init__(self):
        GameObject.__init__(self)
        self.size = (64,64)
        self.load_images()
        self.joystick = 0
        self.UP, self.RIGHT = 0, 0
        self.anim_counter = 0
        if pygame.joystick.get_count() != 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
    def loop(self, screen):
        # check events (with joystick)
        for event in pygame.event.get(): 
            if (self.joystick != 0):
                if (event.type == JOYHATMOTION):
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
                elif event.type == JOYAXISMOTION:
                    if(self.joystick.get_axis(1)<-0.9):
                        self.UP = 1
                    else:
                        self.UP = 0
                    if(self.joystick.get_axis(0)>0.9):
                        self.RIGHT = 1
                    else:
                        self.RIGHT = 0
            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_w:
                    self.UP = 1
                elif event.key == K_DOWN:
                    # DOWN
                    pass
                elif event.key == K_RIGHT or event.key == K_d:
                    self.RIGHT = 1
                elif event.key == K_LEFT:
                    # LEFT
                    pass
            if event.type == KEYUP:
                if event.key == K_UP or event.key == K_w:
                    self.UP = 0
                elif event.key == K_DOWN:
                    # DOWN
                    pass
                elif event.key == K_RIGHT or event.key == K_d:
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
                    
                        
        # set animation and velocity
        if self.UP:
            for name in self.jump_files:
                if name.find('hero1.png') != -1:
                    self.img = name
                    break
        elif self.RIGHT:
            #animation
            img_move = ['', '', '']
            for name in self.move_files:
                if name.find('hero1.png') != -1:
                    img_move[0] = name
                elif name.find('hero2.png') != -1:
                    img_move[1] = name
                elif name.find('hero3.png') != -1:
                    img_move[2] = name
            a = self.img == img_move[0]
            b = self.img == img_move[1]
            c = self.img == img_move[2]
            d = a or b or c
            time = (self.anim_counter > 2)
            if not d:
                self.img = img_move[0]
            else:
                if time:
                    if a:
                        self.img = img_move[1]
                    elif b:
                        self.img = img_move[2]
                    elif c:
                        self.img = img_move[0]
                    self.anim_counter = 0
                else:
                    self.anim_counter += 1
            #move the player
            engine.level_manager.level.physics.move(self,5)
                
        else:
            for name in self.still_files:
                if name.find('hero1.png') != -1:
                    self.img = name
                    break
            #stop the player

            engine.level_manager.level.physics.move(self,0)
        #reset angle
        engine.level_manager.level.physics.set_angle(self,0)
        # show the current img
        self.pos = (int(self.pos[0]), int(self.pos[1]))
        self.img_manager.show(self.img, screen, (0,0))
        engine.level_manager.level.screen_pos = self.pos
        
        
if __name__ == '__main__':
    p = Player()
    p.load_images()
