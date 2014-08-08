from animation.animation_main import Animation
from engine.const import log, CONST
from game_object.image import Image
from json_export.json_main import get_element

__author__ = 'Elias'

class Cat(Image):
    def __init__(self,pos,size=None, angle=0, relative=False, path="", parallax_factor=1.0, move=False):
        Image.__init__(self,
                       pos,
                       size=size,
                       angle=angle,
                       relative=relative,
                       path=path,
                       parallax_factor=parallax_factor)
        self.move = move

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

        move = get_element(image_data,"move")
        if move is None:
            move = False

        image = Cat(pos, size=size, angle=angle,path=path,parallax_factor=parallax_factor,move=move)

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