from engine import level_manager
from engine.vector import Vector2
from game_object.game_object_main import GameObject
from json_export.json_main import get_element
from render_engine.img_manager import img_manager

__author__ = 'efarhan'

class Ground(GameObject):
    def __init__(self,
                 pos,
                 nmb_size):
        GameObject.__init__(self)
        self.pos = pos
        self.nmb_size = nmb_size #nmb_size for 32x12
        self.size = nmb_size*Vector2(32,12)+Vector2(24,12)
        self.init_image()
    def init_image(self):
        self.top_left = img_manager.load_image("data/sprites/ground/GroundTopCornerLeft.png")
        self.top_right = img_manager.load_image("data/sprites/ground/GroundTopCornerRight.png")
        self.top = img_manager.load_image("data/sprites/ground/GroundTop.png")
        self.left = img_manager.load_image("data/sprites/ground/GroundSideLeft.png")
        self.right = img_manager.load_image("data/sprites/ground/GroundSideRight.png")
        self.ground = img_manager.load_image("data/sprites/ground/GroundFill.png")

    def loop(self,screen,lock):
        pos = self.pos-level_manager.level.screen_pos

        img_manager.show_image(self.top_left,screen,pos,new_size=Vector2(12,12))
        img_manager.show_image(self.top_right,screen,pos+Vector2(12+self.nmb_size.x*32,0),new_size=Vector2(12,12))
        for i in range(self.nmb_size.x):
            img_manager.show_image(self.top,screen,pos+Vector2(12+i*32,0),new_size=Vector2(32,12))
            for j in range(self.nmb_size.y):
                img_manager.show_image(self.ground,screen,pos+Vector2(12+i*32,12+j*12),new_size=Vector2(32,12))
        for j in range(self.nmb_size.y):
            img_manager.show_image(self.left, screen,pos+Vector2(0,12+j*12),new_size=Vector2(12,12))
            img_manager.show_image(self.right, screen,pos+Vector2(12+self.nmb_size.x*32,12+j*12),new_size=Vector2(12,12))
    @staticmethod
    def parse_image(json_data, pos, size, angle):
        nmb_size = get_element(json_data,"nmb_size")
        return Ground(Vector2(pos), Vector2(nmb_size))