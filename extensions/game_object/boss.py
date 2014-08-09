from animation.animation_main import Animation
from engine import level_manager
from engine.const import log, CONST
from engine.init import engine
from engine.vector import Vector2
from game_object.image import Image
from json_export.json_main import get_element
from render_engine.img_manager import img_manager

__author__ = 'Elias'

class Boss(Image):
    def loop(self, screen):
        Image.loop(self,screen)

        if self.anim.boum:
            print self.anim.explosion.index
            self.anim.explosion.update_animation(state='boum')
            explosion_pos = Vector2()
            if self.anim.player.anim.direction:
                explosion_pos = self.anim.player.pos + engine.screen_size * self.anim.player.screen_relative_pos + Vector2(self.anim.player.size.x,0)
            else:
                explosion_pos = self.anim.player.pos + engine.screen_size * self.anim.player.screen_relative_pos - Vector2(self.anim.player.size.x,0)
            img_manager.show_image(self.anim.explosion.img, engine.screen, pos=explosion_pos-level_manager.level.screen_pos,new_size=Vector2(36,36))
            if self.anim.explosion.index == 6:
                self.anim.boum = False

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


        image = Boss(pos, size=size, angle=angle,path=path,parallax_factor=parallax_factor)

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