import sfml

from engine.const import log
from render_engine.img_manager import ImgManager
from engine.init import engine
from engine.vector import Vector2

from render_engine.snd_manager import snd_manager

__author__ = 'Elias, Tenchi'


class TextBox():
    def __init__(self):

        self.lines = [""]

        self.time = 0
        self.finished = False
        self.slide = False

        self.size = (152, 36)
        self.buffer = sfml.RenderTexture(*self.size)

        self.font = sfml.Font.from_file("data/font/SILKWONDER.ttf")
        self.texts = []

        self.sound = snd_manager.load_sound("data/sound/Text.wav")

        self.rect = sfml.RectangleShape((self.size[0] - 2, self.size[1] - 2))
        self.rect.move((1,1))
        self.rect.fill_color = sfml.Color(170, 170, 170)
        self.rect.outline_color = sfml.Color(85, 85, 85)
        self.rect.outline_thickness = 4
        self.current = 0
        self.line_counter = 0
        # self.char_counter = 0
        self.current_index = 0

    def set_text(self,speaker, text):
        from textwrap import wrap

        self.lines = wrap(text, 35)

        self.time = 0
        self.finished = False
        self.slide = False

        self.size = (152, 36)
        self.texts = [None for i in xrange(3)]
        self.texts[0] = sfml.Text(speaker.upper(), self.font, 8)
        for i in xrange(3):
            if self.texts[i] is not None:
                self.texts[i].color = sfml.Color.BLACK
                self.texts[i].position = (4 + (1 if i > 0 else 0) * 8, 4 + 10*i)
        self.current = 0
        self.line_counter = 0
        self.current_index = 0

    def swap(self):
        self.current = 1 - self.current

    def loop(self):
        self.buffer.draw(self.rect)
        if (self.slide):
            self.texts[(1 - self.current) + 1].move((0, -1))
            if (self.time == 10):
                self.slide = False
                self.time = 0

        elif (self.time == 6 and not(self.finished)):

            self.time = 0
            # Add a letter
            lenA0 = self.current_index
            lenA1 = len(self.lines[self.line_counter])
            if (lenA0 < lenA1):
                if lenA0 != 0:
                    new_string = self.lines[self.line_counter][0:lenA0+1]
                    new_text = sfml.Text(new_string, self.font, 8)

                    new_text.position = (4 + (1 if self.current+1 > 0 else 0) * 8, 4 + 10*(self.current+1))

                    new_text.color = sfml.Color.BLACK
                    self.texts[self.current + 1] = new_text

                    # if (char != " " and self.char_counter % 1 == 0):
                    snd_manager.play_sound(self.sound)
                self.current_index += 1
                # self.char_counter += 1
                # if (char == " "):
                #     self.char_counter = 0
            else:
                self.current_index = 0
                self.swap()
                self.line_counter += 1
                if (self.line_counter == len(self.lines)):
                    self.finished = True
                if (self.line_counter >= 2):
                    self.texts[self.current + 1] = None
                    self.slide = True

        for t in self.texts:
            if t is not None:
                self.buffer.draw(t)

        self.buffer.display()
        self.time += 1
        spr = sfml.Sprite(self.buffer.texture)
        spr.position = (8, 8)
        return spr

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
        if name is None:
            return None
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
        self.buffer.draw(drawing_rect)

