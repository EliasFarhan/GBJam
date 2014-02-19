'''
Created on 11 sept. 2013

@author: efarhan
'''

from engine.image_manager import  show_image, load_image, get_size,\
    load_image_with_size
from animation.animation import Animation
from engine.init import get_screen_size
from engine.rect import Rect
from game_object.game_object import GameObject
from engine.const import pookoo,log
if pookoo:
    import texture

class Image(GameObject):
    def __init__(self,path,pos,screen_relative_pos=None,size=None,angle=0):
        GameObject.__init__(self)
        self.img = 0
        self.angle = 0
        self.pos = pos
        self.path = path
        self.size = size
        self.screen_relative_pos = None
        self.center_image = False
        self.init_image()
    def init_image(self):
        if self.size == None:
            self.img = load_image(self.path)
            self.size = get_size(self.img)
        else:
            self.img = load_image_with_size(self.path, self.size)
        self.rect = Rect(self.pos, self.size)
    def loop(self, screen, screen_pos):
        pos = self.pos
        if self.screen_relative_pos != None: 
            pos = (pos[0]+self.screen_relative_pos[0]*get_screen_size()[0],
                   pos[1]+self.screen_relative_pos[1]*get_screen_size()[1])
        factor = 1
        if pookoo:
            
            factor = self.size[0]/texture.size(self.img)[0]
            log(str(texture.size(self.img))+" "+str(self.size))
        show_image(self.img, screen, (pos[0]-screen_pos[0],pos[1]-screen_pos[1]),factor=factor,center_image=self.center_image)
        
class AnimImage(Image):
    '''Can be animated if a directory is given,
    if a png file is given, it will load it
    to load several file, like player do not call this constructor'''
    def __init__(self,path,pos,size=None,angle=0):
        Image.__init__(self)
        self.anim = Animation()
        self.init_image()
    def init_image(self):
        '''init only one directory or one image,
        for several directories, please set manually
        animation class before and call directly anim.load_images'''
        self.anim.path_list = [self.path]
        self.anim.load_images(self.size)
        if self.size == None:
            self.size = self.anim.size
        self.rect = Rect(self.pos, self.size)
    def loop(self,screen,screen_pos):
        
        self.anim.update_animation()
        self.img = self.anim.img
        Image.loop(self, screen, screen_pos)
        
        
        


