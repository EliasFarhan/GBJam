import sfml

from engine.const import log
from render_engine.img_manager import ImgManager
from engine.init import engine
from engine.vector import Vector2


__author__ = 'Elias, Tenchi'


class SFMLImgManager(ImgManager):
    def __init__(self):
        ImgManager.__init__(self)
        self.buffer = sfml.RenderTexture(160+8, 144+8)

    def clear_screen(self, screen):
        self.buffer.clear(sfml.Color.WHITE)

    @staticmethod
    def get_size(image):
        return Vector2(image.texture.size)

    def load_image(self, name, tmp=False):
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
            if tmp:
                self.tmp_images.append(name)

        return sfml.Sprite(self.img_name[name])

    def show_image(self, image, screen, pos, angle=0, center=False,
                   new_size=None, center_image=False,flip=False):
        if image is None:
            return
        try:
            sprite = image

            if angle != 0:
                sprite.rotation = angle

            if isinstance(sprite, sfml.Sprite):
                if flip:
                    sprite.texture_rectangle = (sfml.Rectangle(sfml.Vector2(sprite.texture.width, 0), sfml.Vector2(-sprite.texture.width, sprite.texture.height)))
                else:
                    sprite.texture_rectangle = (sfml.Rectangle(sfml.Vector2(0, 0), sfml.Vector2(sprite.texture.width, sprite.texture.height)))

            sprite.position = pos.get_int_tuple()
            sprite.position += 4
            self.buffer.draw(sprite)

        except KeyError:
            pass

    def draw_rect(self, screen, screen_pos, rect, color, angle=0):
        drawing_rect = sfml.RectangleShape()
        origin_pos = engine.get_origin_pos()
        screen_diff_ratio = engine.get_ratio()
        drawing_rect.position = (origin_pos + ( rect.pos - screen_pos) * screen_diff_ratio).get_tuple()

        drawing_rect.rotation = angle
        drawing_rect.size = (rect.size * screen_diff_ratio).get_tuple()
        if len(color) == 4:
            drawing_rect.fill_color = sfml.Color(color[0], color[1], color[2], color[3])
        elif len(color) == 3:
            drawing_rect.fill_color = sfml.Color(color[0], color[1], color[2])
        screen.draw(drawing_rect)

