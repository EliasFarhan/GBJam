'''
Created on 11 sept. 2013

@author: efarhan
'''

from animation.animation_main import Animation
from animation.player_animation import PlayerAnimation

from engine.init import engine
from engine.rect import Rect
from game_object.game_object_main import GameObject
from engine.const import log, CONST
from json_export.json_main import get_element
from engine.vector import Vector2
from render_engine.img_manager import img_manager


class Image(GameObject):
    def __init__(self,
                 pos,
                 size=None,
                 angle=0,
                 relative=False,
                 path="",
                 parallax_factor=1.0):
        GameObject.__init__(self)
        self.anim = None
        self.flip = False
        self.img = None
        self.angle = angle
        if not isinstance(pos, Vector2) and ( isinstance(pos[0], list) or isinstance(pos[0], tuple)):
            self.pos = Vector2(pos[0])
            self.screen_relative_pos = Vector2(pos[1])
        else:
            self.pos = Vector2(pos)
        self.path = path
        if size is not None:
            self.size = Vector2(size)
        self.screen_relative = relative
        
        self.center_image = False
        self.tmp = False
        self.show = True
        self.parallax_factor = parallax_factor
        self.update_rect()

    def init_image(self,size=None):
        if self.anim:
            self.anim.load_images(size,self.tmp)
        else:
            self.img = img_manager.load_image(self.path, self.tmp)
            if self.size is None:
                self.size = Vector2(img_manager.get_size(self.img))
            self.rect = Rect(self.pos, self.size)

    def loop(self, screen):
        if self.anim:
            self.anim.update_animation()
            self.img = self.anim.img
            try:
                self.show = (self.anim.invincibility % (self.anim.show_frequency*2)) < self.anim.show_frequency
            except AttributeError:
                pass
        pos = Vector2()
        if self.pos:
            pos = self.pos
        
        if self.screen_relative_pos is not None:
            pos = pos + self.screen_relative_pos * engine.get_screen_size()

        if self.screen_relative:
            pos = self.pos
        else:
            from engine import level_manager
            pos -= level_manager.level.screen_pos * Vector2(self.parallax_factor,1.0)
            if pos.x > 160 or pos.x + self.size.x < 0:
                return
        
        center_image = False
        try:
            center_image = self.center_image
        except AttributeError:
            pass

        if self.show:
            img_manager.show_image(self.img,
                   screen,
                   pos,
                   new_size=self.size,
                   center_image=center_image,
                   angle=self.angle,
                   flip=self.flip)

        try:
            img_manager.show_image(self.anim.deal_with_it,
                                   screen,
                                   pos+self.anim.deal_pos+self.anim.deal_delta,
                                   new_size=Vector2(32,32))
        except AttributeError:
            pass
        GameObject.loop(self, screen)

    @staticmethod
    def parse_image(image_data, pos, size, angle):
        if pos is None:
            log("Invalid arg pos not defined for Image",1)
            return None
        path = get_element(image_data, "path")
        if path is not None:
            path = CONST.path_prefix+path

        parallax_factor = get_element(image_data, "parallax_factor")
        if parallax_factor is None:
            parallax_factor = 1.0


        image = Image(pos, size=size, angle=angle,path=path,parallax_factor=parallax_factor)

        tmp = get_element(image_data, "tmp")
        if tmp is not None:
            image.tmp = tmp
        else:
            image.tmp = False

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
        


