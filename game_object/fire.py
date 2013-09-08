'''
Created on 8 sept. 2013

@author: efarhan
'''
from game_object import GameObject
from Box2D import *
from physics.physics import pixel2meter

class FireTube(GameObject):
    def __init__(self, screen_size,pos_a, physics,length,vertical=False,angle=0):
        GameObject.__init__(self, physics)
        self.angle = angle
        self.img = []
        self.size = (32,32)
        self.length = length
        self.pos = pos_a
        self.anim_counter = 0
        self.vertical = vertical
        self.line_index = 1
        self.load_images()
        self.init_physics()
    def load_images(self):
        path = 'data/sprites/fire/'
        box = path+'box.png'
        firemid = path+'firemid.png'
        fire = path+'fire.png'
        self.img.append(self.img_manager.load_with_size(box, (self.size[1],self.size[1])))
        self.img.append(self.img_manager.load_with_size(firemid, self.size))
        self.img.append(self.img_manager.load_with_size(fire, self.size))             
    def loop(self,screen,screen_pos):
        self.img_manager.show(self.img[0], screen, (self.pos[0]-screen_pos[0],self.pos[1]-screen_pos[1]))
        if(self.anim_counter == 3):
            if self.line_index == 1:
                self.line_index = 2
            else:
                self.line_index = 1
            self.anim_counter = 0
        else:
            self.anim_counter += 1
        self.img_manager.show(self.img[self.line_index],screen,(self.pos[0]+self.size[0]/2+self.size[1]/2-screen_pos[0],self.pos[1]-screen_pos[1]))
        self.img_manager.show(self.img[0],screen,(self.pos[0]+self.size[0]+self.size[1]-screen_pos[0],self.pos[1]-screen_pos[1]))
    def init_physics(self):
        pos_box1 = self.pos
        index = self.physics.add_static_box(pos_box1, (self.size[1],self.size[1]))
        self.box = self.physics.static_objects[index]
        #add other box
        pos_box2 = (self.size[0]+self.size[1],0)
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(pixel2meter(self.size[1]/2.0),pixel2meter(self.size[1]/2.0),b2Vec2(pixel2meter(pos_box2[0]),pixel2meter(pos_box2[1])),0)
        fixture_def = b2FixtureDef()
        fixture_def.shape = polygon_shape
        fixture_def.density = 1
        self.box.CreateFixture(fixture_def)
        #add electricity sensor
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(pixel2meter(self.size[0]/2.0),pixel2meter(self.size[1]/2.0-2),b2Vec2(pixel2meter(self.size[1]/2.0+self.size[0]/2.0),pixel2meter(0)),0)
        fixture_def = b2FixtureDef()
        fixture_def.shape = polygon_shape
        fixture_def.density = 1
        fixture_def.isSensor = True
        self.elec_sensor_fixture = self.box.CreateFixture(fixture_def)
        self.elec_sensor_fixture.userData = 6