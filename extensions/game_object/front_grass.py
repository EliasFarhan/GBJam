from engine import level_manager
from engine.vector import Vector2
from game_object.game_object_main import GameObject
from json_export.json_main import get_element
from render_engine.img_manager import img_manager

__author__ = 'efarhan'

class FrontGrass(GameObject):
    def __init__(self,
                 pos,
                 nmb_size):
        GameObject.__init__(self)
        self.pos = pos
        self.nmb_size = nmb_size #nmb_size for 47x27
        self.diff = 10
        self.init_image()

    def init_image(self):
        self.img = img_manager.load_image("data/sprites/foreground/LongGrass.png")

    def loop(self,screen):
        pos = self.pos-level_manager.level.screen_pos
        for i in range(self.nmb_size):
            img_manager.show_image(self.img,screen,pos+Vector2(i*(47-self.diff),0),new_size=Vector2(47,27))

    @staticmethod
    def parse_image(json_data, pos, size, angle):
        nmb_size = get_element(json_data,"nmb_size")
        return FrontGrass(Vector2(pos), nmb_size)