import sfml

from engine import level_manager
from engine.const import CONST, log
from engine.init import Engine
from render_engine.input import input_manager
from engine.level_manager import get_level
from engine.vector import Vector2



__author__ = 'Elias'


class SFMLEngine(Engine):
    def init_screen(self):
        self.W, self.H = 800, 720 # 160*144 * 4 + spaces

        desktop = sfml.VideoMode.get_desktop_mode()
        if CONST.debug:
            desktop = sfml.VideoMode(self.W, self.H)
        style = sfml.Style.DEFAULT
        if CONST.fullscreen and not CONST.debug:
            style = sfml.Style.FULLSCREEN
        self.screen = sfml.RenderWindow(desktop, 'Kudu Window', style)
        self.real_screen_size = Vector2(self.screen.size)
        self.screen_diff_ratio = self.real_screen_size / self.screen_size

        input_manager.init()


        # self.x0, self.y0 = self.get_origin_pos().get_int_tuple()
        # self.bg = sfml.Image.create(self.W - (self.x0 * 2), self.H - (self.y0 * 2), sfml.Color.BLACK)
        self.bg = sfml.RenderTexture(self.W, self.H)
        #todo gradient
        # for x in xrange(self.W):
        #     for y in xrange(self.H):
        #         self.bg[x,y] = sfml.Color.WHITE

        shader_x5_src = """

        uniform sampler2D texture;

        void main() {
            gl_FragColor = gl_Color * texture2D(texture, gl_TexCoord[0].xy);

            //vec4 rgb = texture2D(texture, gl_TexCoord[0].xy);
            //vec4 intens;
            //if (fract(gl_FragCoord.y * 0.25) > 0.5)
            //    intens = vec4(0.0);
            //else
            //    intens = smoothstep(0.2,0.8,rgb) + normalize(vec4(rgb.xyz,1.0));
            //float level = (4.0-gl_TexCoord[0].z)*0.19;
            //gl_FragColor = intens * (0.5-level) + rgb * 1.1;
        }

        """

        vertex_passthrough = """
        void main(void) {
            gl_Position = ftransform();
            gl_TexCoord[0] = gl_MultiTexCoord0;

        }
        """

        self.shader_x5 = sfml.Shader.from_memory(vertex=vertex_passthrough, fragment=shader_x5_src)
        self.states = sfml.RenderStates(shader=self.shader_x5)

    def init_level(self):
        from levels.loading_screen import LoadingScreen

        if CONST.debug:
            level_manager.switch_level(LoadingScreen())
        else:
            Engine.init_level(self)

    def pre_update(self):
        pass
        # self.screen.display()

    def post_update(self):
        from render_engine.img_manager import img_manager

        # self.screen.clear(sfml.Color.WHITE)

        # self.bg.clear(sfml.Color.WHITE)

        buf = img_manager.buffer
        buf.display()
        tex = buf.texture
        # img = tex.to_image()

        self.shader_x5.set_texture_parameter("texture", tex)

        rect = sfml.RectangleShape((self.W, self.H))
        self.screen.draw(rect, self.states)

        # W, H = 800, 600

        # x0, y0 = self.get_origin_pos().get_int_tuple()
        # w = (W - (x0 * 2)) / 160
        # gap = 1

        # bg = sfml.Image.create(W - (x0 * 2), H - (y0 * 2), sfml.Color.BLACK)

        # bgx0 = (W - (x0 * 2) - (w * 160)) / 2
        # bgy0 = (H - (y0 * 2) - (w * 144)) / 2

        # print "A"

        # for x in xrange(self.bg.width):
        #     for y in xrange(self.bg.height):
        #         self.bg[x,y] = sfml.Color((1.0*x/self.bg.width)*255, (1.0*y/self.bg.height)*255, 127)

        # rect = sfml.RectangleShape((4, 4))

        # for x in xrange(img.width):
        #     for y in xrange(img.height):
        #         c = img[x,y]
                # for i in xrange(4):
                #     for j in xrange(4):
                #         self.bg[x+i, y+j] = c
                # self.bg[x*4:x*4+4, y] = c
                # rect.fill_color = c
                # rect.position = (5*x, 5*y)

                # self.bg.draw(rect)

        # spr = sfml.Sprite(self.bg.texture)
        # spr.position = (self.x0, self.y0)
        # self.screen.draw(spr)

        # spr.position = (self.get_origin_pos() * self.get_ratio()).get_int_tuple()

        buf.clear(sfml.Color.WHITE)

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

