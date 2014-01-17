'''
Created on 19 dec. 2013

@author: efarhan
'''

from engine.const import cuted_size
from engine.init import get_screen_size
from engine.image_manager import load_image, get_image
import pygame
class DividedImage():
    def __init__(self, path, pos):
        self.pos = pos
        self.path = path
        self.imgs = []
        self.load_images()
    def load_images(self):
        if self.path != None:
            self.img_index = load_image(self.path)
            self.size = get_image(self.img_index).get_size()
            self.divide_images(get_image(self.img_index), self.imgs)
    def divide_images(self, img, container):
        self.cuted_size = cuted_size
        nmb_img = (img.get_size()[0]/self.cuted_size[0],img.get_size()[1]/self.cuted_size[1])
        for i in range(nmb_img[0]+1):
            row = []
            for j in range(nmb_img[1]+1):
                size_x = 0
                size_y = 0
                if(i == nmb_img[0]):
                    size_x = img.get_size()[0]-nmb_img[0]*self.cuted_size[0]
                else:
                    size_x = self.cuted_size[0]
                if(j == nmb_img[1]):
                    size_y = img.get_size()[1]-nmb_img[1]*self.cuted_size[1]
                else:
                    size_y = self.cuted_size[1]
                rect = pygame.Rect((0,0),(size_x,size_y))
                rect = rect.move(self.cuted_size[0]*i,self.cuted_size[1]*j)
                row.append(img.subsurface(rect))
            container.append(row)
    def loop(self, screen, screen_pos,new_pos=(0,0)):
        if self.path != None:
            self.show(screen, screen_pos,self.imgs,new_pos)
    def show(self,screen,screen_pos,imgs,new_pos):
        i = 0
        for row in self.imgs:
            j = 0
            for img in row:
                pos = (0,0)
                if new_pos == (0,0):
                    pos = self.pos
                else:
                    pos = new_pos
                pos = (pos[0]+(i)*self.cuted_size[0],pos[1]+(j)*self.cuted_size[1])
                
                rect = pygame.Rect((-pos[0]+screen_pos[0],-pos[1]+screen_pos[1]),get_screen_size())
                n = False
                if rect.colliderect(img.get_rect()):
                    #show img
                    n = True
                    screen.blit(img, (pos[0]-screen_pos[0],pos[1]-screen_pos[1]))
                j+=1
            i+=1