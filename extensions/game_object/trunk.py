from engine import level_manager
from engine.vector import Vector2
from game_object.game_object_main import GameObject
from json_export.json_main import get_element
from render_engine.img_manager import img_manager

__author__ = 'efarhan'

class Trunk(GameObject):
    def __init__(self,
                 pos,
                 nmb_size):
        GameObject.__init__(self)
        self.pos = pos
        self.nmb_size = nmb_size #nmb_size for 32x12
        self.size = Vector2(24+16*nmb_size,36)
        self.init_image()
    def init_image(self):
        self.right = img_manager.load_image("data/sprites/trunk/TrunkSideRight.png")
        self.left = img_manager.load_image("data/sprites/trunk/TrunkSideLeft.png")
        self.fill = img_manager.load_image("data/sprites/trunk/TrunkFill.png")

    def loop(self,screen):
        pos = self.pos-level_manager.level.screen_pos

        img_manager.show_image(self.left,screen,pos,new_size=Vector2(12,36))
        img_manager.show_image(self.right,screen,pos+Vector2(12+self.nmb_size*16,0),new_size=Vector2(12,36))
        for i in range(self.nmb_size):
            img_manager.show_image(self.fill,screen,pos+Vector2(12+i*16,0),new_size=Vector2(16,36))
    @staticmethod
    def parse_image(json_data, pos, size, angle):
        nmb_size = get_element(json_data,"nmb_size")
        return Trunk(Vector2(pos), nmb_size)