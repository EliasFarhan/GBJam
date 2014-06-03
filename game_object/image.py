'''
Created on 11 sept. 2013

@author: efarhan
'''

from engine.image_manager import  show_image, load_image, get_size
from animation.animation_main import Animation
from engine.init import get_screen_size
from engine.rect import Rect
from game_object.game_object_main import GameObject
from engine.const import log, CONST
from json_export.json_main import get_element
from engine.vector import Vector2


class Image(GameObject):
    def __init__(self, path, pos, screen_relative_pos=None, size=None, angle=0,relative=False):
        GameObject.__init__(self)
        self.img = None
        self.angle = angle
        self.pos = Vector2(pos)
        self.path = path
        self.size = Vector2(size)
        if screen_relative_pos:
            self.screen_relative_pos = Vector2(screen_relative_pos)
        else:
            self.screen_relative_pos = Vector2()
        self.screen_relative = relative
        
        self.center_image = False
        if self.path != '':
            self.init_image()
        self.update_rect()

    def init_image(self):
        self.img = load_image(self.path)
        if self.size is None:
            self.size = Vector2(get_size(self.img))
        self.rect = Rect(self.pos, self.size)

    def loop(self, screen, screen_pos):
        pos = Vector2()
        if self.pos:
            pos = self.pos
        
        if self.screen_relative_pos is not None:
            pos = pos+self.screen_relative_pos*get_screen_size()

        #TODO: with screen_relative_pos
        if self.screen_relative:
            pos = self.pos
        else:
            pos = pos - screen_pos * self.screen_factor
        
        center_image = False
        try:
            center_image = self.center_image
        except AttributeError:
            pass
        i = 0
        if self.img_loop:
            i = int((screen_pos.x-self.pos.x)/(self.size.x/self.screen_factor))
            
        show_image(self.img,
                   screen,
                   pos+self.size/self.screen_factor*i,
                   new_size=self.size,
                   center_image=center_image,
                   angle=self.angle)
        '''Looping image, for background for example'''
        if self.img_loop and pos.x+(i+1)*self.size.x/self.screen_factor < screen_pos.x+get_screen_size().x:
            show_image(self.img,
                       screen,
                       pos+self.size/self.screen_factor*(i+1),
                       new_size=self.size,
                       center_image=center_image,
                       angle=self.angle)
        GameObject.loop(self, screen, screen_pos)
    @staticmethod
    def parse_image(image_data,pos,size,angle):
        path = get_element(image_data, "path")
        if path and pos:
            path = CONST.path_prefix+path
            image = Image(path, pos, None, size, angle)
            screen_factor = get_element(image_data, "screen_factor")
            if screen_factor:
                image.screen_factor = screen_factor
            img_loop = get_element(image_data, "loop")
            if img_loop:
                image.img_loop = True
            return image
        else:
            log("Invalid arg path not defined for Image",1)
            return None


class AnimImage(Image):
    '''Can be animated if a directory is given,
    if a png file is given, it will load it
    to load several file, like player do not call this constructor'''
    def __init__(self):
        GameObject.__init__(self)
        self.img = 0
        self.anim = None

    def loop(self,screen,screen_pos):
        if self.anim:
            self.anim.update_animation()
            self.img = self.anim.img
        Image.loop(self, screen, screen_pos)

    @staticmethod
    def parse_image(image_data, pos, size, angle):
        
        image = AnimImage()
        '''TODO: parse correctly position, depending on
        type:
        [x,y] pos
        [[x,y],[x',y'] pos, screen_relative_pos'''
        if isinstance(pos[0], list) or isinstance(pos[0], tuple):
            image.pos = Vector2(pos[0])
            image.screen_relative_pos = Vector2(pos[1])
        else:
            image.pos = Vector2(pos)
        image.size = Vector2(size)
        log("PLAYER SIZE:"+str( image.size.get_tuple()))
        anim_data = get_element(image_data, "anim")
        if anim_data:
            image.anim = Animation.parse_animation(anim_data, image)
            if image.anim:
                image.anim.load_images(size)
        return image

def MaskImage():
    def __init__(self):
        self.masks = [] #we can have different masks combined
        


