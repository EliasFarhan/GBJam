from engine import level_manager
from engine.vector import Vector2
from game_object.game_object_main import GameObject
from json_export.json_main import get_element
from physics_engine.physics_manager import physics_manager, BodyType
from render_engine.img_manager import img_manager

__author__ = 'efarhan'


class Stump(GameObject):
    def __init__(self,
                 pos,
                 nmb_size):
        GameObject.__init__(self)
        self.pos = pos
        self.nmb_size = nmb_size #nmb_size for 32x12
        self.size = Vector2(49,4+14*nmb_size+12)
        self.init_image()
        self.body = physics_manager.add_body(pos=self.pos+Vector2(7,3)+Vector2(31, self.size.y)/2,body_type=BodyType.static)
        physics_manager.add_box(body=self.body, pos=Vector2(),size=Vector2(31, self.size.y)/2,data=12)
    def init_image(self):
        self.base = img_manager.load_image("data/sprites/stump/StumpBase.png")
        self.top = img_manager.load_image("data/sprites/stump/StumpTop.png")
        self.fill = img_manager.load_image("data/sprites/stump/StumpFill.png")

    def loop(self,screen):
        pos = self.pos-level_manager.level.screen_pos

        img_manager.show_image(self.top,screen,pos+Vector2(7,0),new_size=Vector2(31,4))
        img_manager.show_image(self.base,screen,pos+Vector2(0,4+self.nmb_size*14),new_size=Vector2(49,12))
        for j in range(self.nmb_size):
            img_manager.show_image(self.fill,screen,pos+Vector2(7,4+14*j),new_size=Vector2(31,14))

    @staticmethod
    def parse_image(json_data, pos, size, angle):
        nmb_size = get_element(json_data,"nmb_size")
        return Stump(Vector2(pos), nmb_size)