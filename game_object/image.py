'''
Created on 11 sept. 2013

@author: efarhan
'''

from engine.img_manager import   img_manager
from animation.animation_main import Animation
from engine.init import engine
from engine.rect import Rect
from game_object.game_object_main import GameObject
from engine.const import log, CONST
from json_export.json_main import get_element
from engine.vector import Vector2


class Image(GameObject):
    def __init__(self,
                 pos,
                 size=None,
                 angle=0,
                 relative=False,
                 path=""):
        GameObject.__init__(self)
        self.anim = None
        self.flip = False
        self.img = None
        self.angle = angle
        if isinstance(pos[0], list) or isinstance(pos[0], tuple):
            self.pos = Vector2(pos[0])
            self.screen_relative_pos = Vector2(pos[1])
        else:
            self.pos = Vector2(pos)
        self.path = path
        self.size = Vector2(size)
        self.screen_relative = relative
        
        self.center_image = False
        self.update_rect()

    def init_image(self,size=None):
        if self.anim:
            self.anim.load_images(size)
        else:
            self.img = img_manager.load_image(self.path)
            if self.size is None:
                self.size = Vector2(img_manager.get_size(self.img))
            self.rect = Rect(self.pos, self.size)

    def loop(self, screen, screen_pos):
        if self.anim:
            self.anim.update_animation()
            self.img = self.anim.img
        pos = Vector2()
        if self.pos:
            pos = self.pos
        
        if self.screen_relative_pos is not None:
            pos = pos + self.screen_relative_pos * engine.get_screen_size()

        if self.screen_relative:
            pos = self.pos
        else:
            pos = pos - screen_pos
        
        center_image = False
        try:
            center_image = self.center_image
        except AttributeError:
            pass
            
        img_manager.show_image(self.img,
                   screen,
                   pos,
                   new_size=self.size,
                   center_image=center_image,
                   angle=self.angle,
                   flip=self.flip)

        GameObject.loop(self, screen, screen_pos)

    @staticmethod
    def parse_image(image_data, pos, size, angle):
        if pos is None:
            log("Invalid arg pos not defined for Image",1)
            return None
        path = get_element(image_data, "path")
        if path is not None:
            path = CONST.path_prefix+path

        image = Image(pos, size=size, angle=angle)


        anim_data = get_element(image_data, "anim")
        if anim_data:
            image.anim = Animation.parse_animation(anim_data, image)
        image.init_image(size)
        return image


"""
class AnimImage(Image):
    '''Can be animated if a directory is given,
    if a png file is given, it will load it
    to load several file, like player do not call this constructor'''
    def __init__(self):
        GameObject.__init__(self)
        self.img = None
        self.anim = None

    def loop(self,screen,screen_pos):
        if self.anim:
            self.anim.update_animation()
            self.img = self.anim.img
        Image.loop(self, screen, screen_pos)

    @staticmethod
    def parse_image(image_data, pos, size, angle):
        
        image = AnimImage()
        '''parse position, depending on
        type:
        [x,y]: pos
        [[x,y],[x',y']: pos, screen_relative_pos'''
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

        return image
"""
class MaskImage(Image):
    def __init__(self):
        self.masks = [] #we can have different masks combined
        


