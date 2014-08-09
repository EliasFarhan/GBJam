import sfml

from engine import level_manager
from engine.const import CONST, log
from engine.init import Engine
from render_engine.input import input_manager
from engine.level_manager import get_level
from engine.vector import Vector2



__author__ = 'Elias, Tenchi'


class SFMLEngine(Engine):
    def init_screen(self):
        # self.res  = (640, 576)
        self.res  = (672, 608)

        desktop = sfml.VideoMode.get_desktop_mode()
        if CONST.debug:
            desktop = sfml.VideoMode(1280, 720)
        style = sfml.Style.DEFAULT
        if CONST.fullscreen and not CONST.debug:
            style = sfml.Style.FULLSCREEN
        self.screen = sfml.RenderWindow(desktop, 'Kudu Window', style)
        self.real_screen_size = Vector2(self.screen.size)
        self.screen_diff_ratio = self.real_screen_size / self.screen_size

        input_manager.init()

        self.col1 = (0.65, 0.69, 0.05)
        self.col2 = (0.13, 0.19, 0.09)
        blur_size = 1.0
        shadow_offs = (0.5, 0.7)


        shader_bg_src = """
            uniform sampler2D texture;
            uniform vec3 col1;
            uniform vec3 col2;
            uniform vec2 res;
            uniform vec2 screen;

            void main() {

                vec2 pos = gl_FragCoord.xy;

                vec4 pixel = texture2D(texture, pos / res);

                pixel.rgb = vec3(col1.r + mix(-1.0, 1.0, pixel.r) * 0.5,
                                 col1.g + mix(-1.0, 1.0, pixel.g) * 0.5,
                                 col1.b + mix(-1.0, 1.0, pixel.b) * 0.5);

                gl_FragColor = pixel;
            }
        """

        shader_x4_src = """
            uniform sampler2D texture;
            uniform vec3 col1;
            uniform vec3 col2;
            uniform vec2 res;
            uniform vec2 screen;

            void main() {

                vec2 pos = gl_FragCoord.xy;

                bool is_on_dot = all(bvec2(mod(pos.x - 0.5, 4.0) > 0.0, mod(pos.y - 0.5, 4.0) > 0.0));

                // If the pixel is on a dot, mix the color
                if (is_on_dot) {
                    vec4 pixel = texture2D(texture, pos / res);
                    float val = (pixel.r + pixel.g + pixel.b) / 3.0;
                    val = pow(val, 0.65);
                    // If white, no alpha
                    float white = val == 1.0 ? 0.0 : 1.0;
                    gl_FragColor = vec4(mix(col2, col1*0.99, val), white);
                }
                // Line
                else {
                    gl_FragColor = vec4(0.0);
                }
            }
        """

        shader_vblur_src = """
            uniform sampler2D texture;
            uniform vec3 col1;
            uniform vec3 col2;
            uniform vec2 res;
            uniform vec2 screen;
            uniform float blurSize;
            uniform vec2 offset;

            void main() {

                vec4 sum = vec4(0.0);

                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x - 4.0*blurSize, gl_FragCoord.y)) / res) * 0.05;
                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x - 3.0*blurSize, gl_FragCoord.y)) / res) * 0.09;
                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x - 2.0*blurSize, gl_FragCoord.y)) / res) * 0.12;
                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x -     blurSize, gl_FragCoord.y)) / res) * 0.15;
                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x,                gl_FragCoord.y)) / res) * 0.18;
                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x +     blurSize, gl_FragCoord.y)) / res) * 0.15;
                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x + 2.0*blurSize, gl_FragCoord.y)) / res) * 0.12;
                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x + 3.0*blurSize, gl_FragCoord.y)) / res) * 0.09;
                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x + 4.0*blurSize, gl_FragCoord.y)) / res) * 0.05;

                gl_FragColor = sum;
            }
        """

        shader_hblur_src = """
            uniform sampler2D texture;
            uniform vec3 col1;
            uniform vec3 col2;
            uniform vec2 res;
            uniform vec2 screen;
            uniform float blurSize;
            uniform vec2 offset;

            void main() {

                vec4 sum = vec4(0.0);

                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x, gl_FragCoord.y - 4.0*blurSize)) / res) * 0.05;
                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x, gl_FragCoord.y - 3.0*blurSize)) / res) * 0.09;
                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x, gl_FragCoord.y - 2.0*blurSize)) / res) * 0.12;
                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x, gl_FragCoord.y -     blurSize)) / res) * 0.15;
                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x, gl_FragCoord.y               )) / res) * 0.18;
                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x, gl_FragCoord.y +     blurSize)) / res) * 0.15;
                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x, gl_FragCoord.y + 2.0*blurSize)) / res) * 0.12;
                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x, gl_FragCoord.y + 3.0*blurSize)) / res) * 0.09;
                sum += texture2D(texture, (offset + vec2(gl_FragCoord.x, gl_FragCoord.y + 4.0*blurSize)) / res) * 0.05;

                float val = (sum.r + sum.g + sum.b) / 3.0;
                val = pow(val, 0.65);
                gl_FragColor = vec4(col2*1.8, (1.0-val)*0.75);
            }

        """

        vertex_passthrough = """
        void main(void) {
            gl_Position = ftransform();
            gl_TexCoord[0] = gl_MultiTexCoord0;

        }
        """

        self.shader_bg = sfml.Shader.from_memory(vertex=vertex_passthrough, fragment=shader_bg_src)
        self.shader_x4 = sfml.Shader.from_memory(vertex=vertex_passthrough, fragment=shader_x4_src)
        self.shader_vb = sfml.Shader.from_memory(vertex=vertex_passthrough, fragment=shader_vblur_src)
        self.shader_hb = sfml.Shader.from_memory(vertex=vertex_passthrough, fragment=shader_hblur_src)
        self.states = sfml.RenderStates()

        self.blocs = sfml.RenderTexture(*self.res)
        self.vblur = sfml.RenderTexture(*self.res)
        self.hblur = sfml.RenderTexture(*self.res)

        from render_engine.img_manager import img_manager

        self.bg = sfml.Texture.from_file("data/sprites/grainy_background.png")
        gbtex = sfml.Texture.from_file("data/sprites/border_square_4x.png")
        self.gb = sfml.Sprite(gbtex)
        self.gb.position = (self.screen.size - gbtex.size) / 2
        self.buf = img_manager.buffer

        self.shader_bg.set_texture_parameter("texture", self.bg)
        self.shader_x4.set_texture_parameter("texture", self.buf.texture)
        self.shader_vb.set_texture_parameter("texture", self.buf.texture)
        self.shader_hb.set_texture_parameter("texture", self.vblur.texture)

        for shader in [self.shader_bg, self.shader_x4, self.shader_vb, self.shader_hb]:
            shader.set_3float_parameter("col1", *self.col1)
            shader.set_3float_parameter("col2", *self.col2)
            shader.set_2float_parameter("res",  *self.res)
            shader.set_2float_parameter("screen",  *self.screen.size)
        self.shader_vb.set_1float_parameter("blurSize", blur_size)
        self.shader_hb.set_1float_parameter("blurSize", blur_size)
        self.shader_vb.set_2float_parameter("offset", *shadow_offs)
        self.shader_hb.set_2float_parameter("offset", *shadow_offs)

        self.dmg = sfml.RenderTexture(*self.res)

        from sfml_img_manager import TextBox

        self.textbox = TextBox()
        self.show_dialog = False


    def init_level(self):
        from levels.loading_screen import LoadingScreen

        if CONST.debug:
            level_manager.switch_level(LoadingScreen())
        else:
            Engine.init_level(self)

    def pre_update(self):
        pass

    def post_update(self):
        # trim 4 pixels all around
        rect = sfml.RectangleShape((4, 152))
        rect.fill_color = sfml.Color.WHITE
        self.buf.draw(rect)
        rect.move((164, 0))
        self.buf.draw(rect)
        rect = sfml.RectangleShape((168, 4))
        self.buf.draw(rect)
        rect.move((0, 148))
        self.buf.draw(rect)
        # test textbox
        if self.show_dialog:
            self.buf.draw(self.textbox.loop())

        clear = sfml.Color(0, 0, 0, 0)
        self.buf.display()

        rect = sfml.RectangleShape(self.res)
        rect.fill_color = clear
        self.dmg.clear()
        self.states.shader = self.shader_bg
        self.dmg.draw(rect, self.states)

        self.states.shader = self.shader_x4
        self.blocs.clear(clear)
        self.blocs.draw(rect, self.states)
        self.blocs.display()

        self.states.shader = self.shader_vb
        self.vblur.clear(clear)
        self.vblur.draw(rect, self.states)
        self.vblur.display()

        self.states.shader = self.shader_hb
        self.hblur.clear(clear)
        self.hblur.draw(rect, self.states)
        self.hblur.display()

        spr = sfml.Sprite(self.hblur.texture)
        self.dmg.draw(spr)
        spr = sfml.Sprite(self.blocs.texture)
        self.dmg.draw(spr)

        self.dmg.display()

        # Whole screen

        rect = sfml.RectangleShape(self.screen.size)
        rect.fill_color = sfml.Color.BLACK
        self.screen.draw(rect)
        spr = sfml.Sprite(self.dmg.texture)
        spr.position = (self.screen.size - self.res) / 2
        self.screen.draw(spr)
        self.screen.draw(self.gb)

        self.buf.clear(sfml.Color.WHITE)

        self.screen.framerate_limit = CONST.framerate
        self.screen.display()

    def get_origin_pos(self):
        origin_pos = Vector2()
        if self.real_screen_size.get_ratio() > self.screen_size.get_ratio():

            origin_pos = Vector2((self.real_screen_size.x -
                                  self.real_screen_size.y *
                                  self.screen_size.get_ratio()) / 2, 0)
        else:
            origin_pos = Vector2(0, (self.real_screen_size.y -
                                     self.real_screen_size.x /
                                     self.screen_size.get_ratio()) / 2)
        return origin_pos

    def get_ratio(self):
        screen_diff_ratio = Vector2()
        if self.real_screen_size.get_ratio() > self.screen_size.get_ratio():
            screen_diff_ratio = self.screen_diff_ratio.y

        else:
            screen_diff_ratio = self.screen_diff_ratio.x
        return screen_diff_ratio

    def exit(self):

        from render_engine.img_manager import img_manager

        img_manager.sanitize_img_manager(remove_all=True)
        self.screen.close()
        Engine.exit(self)

    def update_event(self):
        """
        Update the states of Input Event
        """
        window = self.screen
        input_manager.update_joy_event()
        for event in window.events:
            input_manager.update_keyboard_event(event)

            if type(event) is sfml.CloseEvent:
                self.finish = True
            elif type(event) is sfml.MouseButtonEvent:

                screen_ratio = float(self.screen_size.y) / Vector2(self.screen.size).y
                from levels.gamestate import GameState

                if get_level().__class__ == GameState:
                    log((Vector2(event.position) * screen_ratio + get_level().screen_pos).get_tuple())
            elif type(event) is sfml.ResizeEvent:
                new_size = event.size

