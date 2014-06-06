"""
Manage images loading, transforming and rendering
"""


from engine.const import CONST, log


class ImgManager():
    def __init__(self):
        self.img_name = {}
        self.permanent_images = []

    def clear_screen(self,screen):
        pass

    def draw_rect(self, screen, screen_pos, rect, color, angle=0):
        pass

    def load_image(self, name, permanent=False):
        pass

    def show_image(self, image, screen, pos, angle=0, center=False, new_size=None, center_image=False):
        pass

    def sanitize_img_manager(self, delete_images=[]):
        del_img_tmp = []
        if not delete_images:
            for img_filename in self.img_name.keys():
                if img_filename not in self.permanent_images:
                    del_img_tmp.append(self.img_name[img_filename])
        else:
            del_img_tmp = delete_images

        for img_filename in del_img_tmp:
            del self.img_name[img_filename]

img_manager = ImgManager()
if CONST.render == 'sfml':
    log("Creating SFMLImgManager")
    from sfml_engine.sfml_img_manager import SFMLImgManager
    img_manager = SFMLImgManager()
elif CONST.render == 'pookoo':
    from pookoo_engine.pookoo_img_manager import PookooImgManager
    img_manager = PookooImgManager
elif CONST.render == 'kivy':
    import kivy
    from kivy.uix.widget import Widget
    from kivy.uix.image import Image


'''
def draw_rect(screen, screen_pos, rect, color, angle=0):
    if not (rect and rect.pos and rect.size and img_manager):
        return
    img_manager.draw_rect(screen, screen_pos, rect, color, angle)
    """
    elif CONST.render == 'pookoo':
        try:
            pookoo.draw.color(color[0],color[1],color[2],color[3])
        except IndexError:
            pookoo.draw.color(color[0],color[1],color[2],255)
        pos = (rect.pos-screen_pos)
        pookoo.draw.move(pos.get_tuple())
        pookoo.draw.rectangle(rect.size.get_int_tuple())
    """


def get_size(image):
    if img_manager is None:
        return None
    return img_manager.get_size(image)
    if CONST.render == 'pookoo':
        return Vector2(image.size())


def load_image(name, permanent=False):
    if img_manager is None:
        return None
    return img_manager.load_image(name, permanent=False)
    """
        elif CONST.render == 'pookoo':
            try:
                if prefix:
                    img_name[name] = pookoo.texture.Texture(CONST.path_prefix+name)
                else:
                    img_name[name] = pookoo.texture.Texture(name)
            except Exception as e:
                log(str(e), 1)
                return None
        elif CONST.render == 'kivy':
            img_name[name] = kivy.core.image.Image.load(filename=name,keep_data=True)

        if permanent:
            permanent_images.append(name)

    elif CONST.render == 'pookoo' :
        return img_name[name]
    elif CONST.render == 'kivy':
        img = Image()
        img.allow_stretch = True
        img.texture = img_name[name].texture
        get_kivy_screen().add_widget(img)
        return img
    """


def show_image(image, screen, pos, angle=0, center=False, new_size=None, center_image=False):
    if img_manager is None:
        return
    img_manager.show_image(image, screen, pos, angle, center, new_size, center_image)
    """try:
        if CONST.render == 'sfml':
            pass
        elif CONST.render == 'pookoo':
            pookoo.draw.move(pos.get_tuple())
            pookoo.draw.scale(new_size.x/get_size(image).x, new_size.y/get_size(image).y)
            image.render()
        elif CONST.render == 'kivy':
            log("SHOW IMAGE "+str(image)+str(new_size.get_tuple()))
            image.x = pos.x
            image.y = pos.y
            if angle != 0:
                pass
            if new_size is not None:
                image.texture_size[0] = new_size.x
                image.texture_size[1] = new_size.y
    except KeyError:
        pass

    """

def generate_mask(masks):
    """TODO: pass several masks as sprite and return a single sprite"""
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

def show_video():
    pass'''