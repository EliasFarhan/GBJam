"""
Created on 9 dec. 2013

@author: efarhan
"""
from engine.img_manager import img_manager
from engine.init import get_screen_size
from engine.rect import Rect
from engine.snd_manager import snd_manager
from engine.vector import Vector2
from game_object.image import Image, AnimImage
from levels.scene import Scene
from engine.const import log, CONST
from network.gamestate_network import NetworkGamestate
from json_export.level_json import load_level
from engine.physics_manager import physics_manager
from levels.editor import Editor
from levels.gui import GUI
from input.mouse_input import show_mouse, get_mouse


class GameState(Scene, Editor, GUI, NetworkGamestate):
    def __init__(self, filename):
        self.bg_color = [0, 0, 0]
        self.player = None
        self.event = {}
        self.filename = filename
        if CONST.debug:
            Editor.__init__(self)
        GUI.__init__(self)

    def init(self, loading=False):

        physics_manager.init_world()
        self.objects = [ [] for i in range(CONST.layers) ]
        self.screen_pos = Vector2()
        self.show_mouse = False
        if self.filename != "":
            log("Loading level " + self.filename)
            if not load_level(self):
                from engine.level_manager import switch_level
                switch_level(Scene())
        self.lock = False
        self.click = False

        log("INIT NETWORK")
        NetworkGamestate.init(self)

        if not loading:
            log("EXECUTE INIT EVENT")
            self.execute_event('on_init')
        log("GAMESTATE INIT OVER")

    def execute_event(self, name):
        log(str(self.event[name]))
        try:
            if self.event[name]:
                self.event[name].execute()
        except KeyError as e:
            log("Error: No such event: %s"%(name)+str(e), 1)

    def reload(self, newfilename):
        self.filename = newfilename
        self.init()

    def loop(self, screen):
        img_manager.draw_rect(screen, Vector2(), Rect(Vector2(),get_screen_size()),self.bg_color)
        snd_manager.update_music_status()
        if CONST.render == 'kivy':
            for layer in self.objects:
                for img in layer:
                    #set img pos outside the screen
                    if isinstance(img, AnimImage):
                        for kivy_img in img.anim.img_indexes:
                            kivy_img.x = -get_screen_size().x
                            kivy_img.y = -get_screen_size().y

        '''Event
        If mouse_click on element, execute its event, of not null'''
        if self.show_mouse:
            show_mouse()
            mouse_pos, pressed = get_mouse()
            if pressed[0] and not self.click:
                event = None
                self.click = True
                for layer in self.objects:
                    for image in layer:
                        if image.check_click(mouse_pos, self.screen_pos):
                            event = image.event
                if event:
                    event.execute()
            elif not pressed[0]:
                self.click = False



        if not self.lock:
            physics_manager.loop()


        '''Show images'''
        if self.player and self.player.anim:
            self.screen_pos = self.player.anim.get_screen_pos()
        remove_image = []
        for i, layer in enumerate(self.objects):
            if i == 2:
                NetworkGamestate.loop(self, screen)
            for j, img in enumerate(layer):
                img.loop(screen, self.screen_pos)
                if img.remove:
                    remove_image.append(img)
        for r in remove_image:
            self.objects[i].remove(r)

        '''GUI'''
        GUI.loop(self, screen)

        '''Editor'''
        if CONST.debug:
            Editor.loop(self, screen, self.screen_pos)

    def exit(self, screen):
        physics_manager.remove_world(physics_manager.current_world)

        Scene.exit(self, screen)
