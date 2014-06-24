from engine.const import log, CONST
from engine.img_manager import ImgManager
from engine.vector import Vector2

__author__ = 'Elias'

import pookoo

class PookooImgManager(ImgManager):
    def __init__(self):
        ImgManager.__init__(self)

    def clear_screen(self,screen):
        pass

    @staticmethod
    def get_size(image):
        return Vector2(image.size())

    def load_image(self, name, tmp=False):
        try:
            self.img_name[name] = pookoo.texture.Texture(CONST.path_prefix+name)
        except Exception as e:
            log(str(e), 1)
            return None
        if tmp:
            self.tmp_images.append(name)
        return self.img_name[name]

    def show_image(self, image, screen, pos, angle=0, center=False, new_size=None, center_image=False):
        #TODO: add the screen ratio
        pookoo.draw.move(pos.get_tuple())
        pookoo.draw.scale(new_size.x/self.get_size(image).x, new_size.y/self.get_size(image).y)
        image.render()

    def draw_rect(self, screen, screen_pos, rect, color=(255,255,255,255), angle=0):
        if not (rect and rect.pos and rect.size):
            return
        try:
            pookoo.draw.color(color[0]/255.0,color[1]/255.0,color[2]/255.0,color[3]/255.0)
        except IndexError:
            pookoo.draw.color(color[0]/255.0,color[1]/255.0,color[2]/255.0,1.0)
        pos = (rect.pos-screen_pos)
        pookoo.draw.move(pos.get_tuple())
        pookoo.draw.rectangle(rect.size.get_int_tuple())