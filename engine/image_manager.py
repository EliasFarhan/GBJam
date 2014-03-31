"""
Manage images loading, transforming and rendering
"""
from engine.const import CONST, log
from engine.init import get_screen_size
from engine.vector import Vector2


if CONST.render == 'sfml':
    import sfml

from math import radians, cos, sin


images = {}
img_name = {}
permanent_images = []


def draw_rect(screen, screen_pos, rect, color, angle=0):
    if not (rect and rect.pos and rect.size):
        return
    if CONST.render == 'sfml':

        drawing_rect = sfml.RectangleShape()
        screen_diff_ratio = float(screen.size.y) / get_screen_size().y
        drawing_rect.position = ((rect.pos - screen_pos) * screen_diff_ratio).get_tuple()

        drawing_rect.rotation = angle
        drawing_rect.size = (rect.size * screen_diff_ratio).get_tuple()
        drawing_rect.fill_color = sfml.Color(color[0], color[1], color[2], color[3])
        screen.draw(drawing_rect)


def fill_surface(surface, r, g, b, a=255):
    if CONST.render == 'sfml':
        surface.clear(sfml.Color(r, g, b))


def sanitize_img_manager():
    for index in images.keys():
        if index not in permanent_images:
            try:
                images.pop(index)
            except KeyError:
                pass


def get_image(index):
    return images[index]


def get_size(index):
    if CONST.render == 'sfml':
        return index.texture.size


def load_image(name, permanent=False):
    try:
        img_name[name]
    except KeyError:
        if CONST.render == 'sfml':
            try:
                img_name[name] = sfml.Texture.from_file(name)
            except IOError as e:
                log(str(e), 1)
                return None
        if permanent:
            permanent_images.append(name)
    if CONST.render == 'sfml':
        return sfml.Sprite(img_name[name])


def load_image_with_size(name, size, permanent=False):
    try:
        img_name[name]
    except KeyError:
        index = load_image(name, permanent)
    if CONST.render == 'sfml':
        return sfml.Sprite(img_name[name])


def show_image(image, screen, pos, angle=0, center=False, new_size=None, rot_func=None, factor=1, center_image=False):
    if image == None:
        return
    try:
        if CONST.render == 'sfml':
            sprite = image
            screen_diff_ratio = float(screen.size.y) / get_screen_size().y
            if new_size:
                text_size = Vector2().tuple2(sprite.texture.size)

                sprite.ratio = (new_size * screen_diff_ratio / text_size).get_tuple()
            if angle != 0:
                sprite.rotation = angle

            sprite.position = (pos * screen_diff_ratio).get_int_tuple()
            screen.draw(sprite)
    except KeyError:
        pass


def generate_mask(masks):
    '''TODO: pass several masks as sprite and return a single sprite'''
    pass


def show_mask_img(screen, bg, mask, bg_pos, mask_pos=(0, 0), bg_size=None, mask_size=None, bg_angle=0, mask_angle=0):
    if CONST.render == 'sfml':
        render_size = None
        if mask_size:
            render_size = mask_size
        else:
            render_size = mask.texture.size
        mask_render = sfml.RenderTexture(render_size[0], render_size[1])
        alpha_states = sfml.RenderStates(sfml.BlendMode.BLEND_MULTIPLY)

        mask_render.clear(sfml.Color(0, 0, 0, 0))
        bg.pos = bg_pos
        if bg_angle != 0:
            bg.rotation = bg_angle
        mask_render.draw(bg)
        if mask_angle != 0:
            mask.rotation = mask_angle

        mask_render.draw(mask, states=alpha_states)
        mask_render.display()
        mask_render_sprite = sfml.Sprite(mask_render.texture)
        mask_render_sprite.position = mask_pos
        screen.draw(mask_render_sprite)


