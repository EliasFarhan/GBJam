import sfml
from engine.const import log, CONST
from engine.img_manager import ImgManager
from engine.init import get_screen_size
from engine.vector import Vector2

__author__ = 'Elias'


class SFMLImgManager(ImgManager):
    def __init__(self):
        ImgManager.__init__(self)

    def clear_screen(self,screen):
        screen.clear()

    def get_size(self,image):
        return Vector2(image.texture.size)

    def load_image(self, name, permanent=False):
        log("Loading image: "+name)
        try:
            self.img_name[name]
        except KeyError:
            try:
                log("Load sfml texture: "+name)
                self.img_name[name] = sfml.Texture.from_file(name)
            except IOError as e:
                log(str(e), 1)
                return None
            if permanent:
                self.permanent_images.append(name)

        return sfml.Sprite(self.img_name[name])

    def show_image(self, image, screen, pos, angle=0, center=False,
                   new_size=None, center_image=False):
        if image is None:
            return
        try:
            sprite = image
            #TODO: Adapt to 4:3 screen or not 16:9
            screen_diff_ratio = float(screen.size.y) / get_screen_size().y
            if new_size:
                text_size = None

                if isinstance(sprite, sfml.Sprite):
                    text_size = Vector2(sprite.texture.size)
                else:
                    text_size = new_size
                sprite.ratio = (new_size * screen_diff_ratio / text_size).get_tuple()
            if angle != 0:
                sprite.rotation = angle

            sprite.position = (pos * screen_diff_ratio).get_int_tuple()
            screen.draw(sprite)

        except KeyError:
            log("Woot")
            pass

    def draw_rect(self, screen, screen_pos, rect, color, angle=0):
        drawing_rect = sfml.RectangleShape()
        screen_diff_ratio = float(screen.size.y) / get_screen_size().y
        drawing_rect.position = ((rect.pos - screen_pos) * screen_diff_ratio).get_tuple()

        drawing_rect.rotation = angle
        drawing_rect.size = (rect.size * screen_diff_ratio).get_tuple()
        if len(color) == 4:
            drawing_rect.fill_color = sfml.Color(color[0], color[1], color[2], color[3])
        elif len(color) == 3:
            drawing_rect.fill_color = sfml.Color(color[0], color[1], color[2])
        screen.draw(drawing_rect)

