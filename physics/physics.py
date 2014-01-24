
from engine.const import move_speed, jump, framerate,jump_step,gravity, log,\
    pybox2d, pookoo
import pypybox2d
if pookoo:
    import physics
else:
    if pybox2d:
        import pypybox2d as b2
        from pypybox2d import world
    else:
        from Box2D import *
from physics.contact_listener import KuduContactListener

ratio = 64/1.5

def pixel2meter(pixels):
    global ratio
    return pixels/ratio
def meter2pixel(meter):
    global ratio
    return meter*ratio
def set_ratio_pixel(new_ratio):
    global ratio
    ratio = new_ratio
    
static_objects = {}
timeStep = 1.0 / framerate
vel_iters, pos_iters = 10,10
index = 1
world = None

def init_physics(gravity_arg=None):
    global world,static_objects,dynamic_objects
    world = None
    gravity_value = 0
    if(gravity_arg == None):
        gravity_value = gravity 
    else:
        gravity_value = gravity_arg
    
    if pybox2d:
        world = b2.World(gravity=(0,gravity_value))
        world.contact_manager = KuduContactListener()
    else:
        world = b2World(gravity=(0,gravity_value))
        world.contactListener = KuduContactListener()

def add_dynamic_object(obj,pos):
    global world
    position = (pixel2meter(pos[0]),pixel2meter(pos[1]))
    dynamic_object = None
    if pybox2d:
        dynamic_object = world.create_dynamic_body(position=position)
    else:
        dynamic_object = world.CreateDynamicBody(position=position)
    dynamic_object.angle = 0
    dynamic_object.fixed_rotation = True
    return dynamic_object

def update_physics():
    global timeStep, vel_iters, pos_iters
    if pybox2d:
        world.step(timeStep, vel_iters, pos_iters)
        world.clear_forces()
    else:
        world.Step(timeStep,vel_iters,pos_iters)
        world.ClearForces()
    
def move(body,vx=None,vy=None):
    dyn_obj = body
    velx,vely= None,None
    if pybox2d:
        velx,vely = dyn_obj.linear_velocity.x,dyn_obj.linear_velocity.y
    else:
        velx,vely = dyn_obj.linearVelocity.x,dyn_obj.linearVelocity.y
    fx,fy=0,0
    if(vx != None):
        velx = vx * move_speed - velx
        fx = dyn_obj.mass * velx / timeStep
    if(vy != None):
        vely = vy * move_speed - vely
        fy = dyn_obj.mass * vely / timeStep
    if pybox2d:
        dyn_obj.apply_force(b2.Vec2(fx,fy),dyn_obj.world_center)
    else:
        dyn_obj.ApplyForce(b2Vec2(fx,fy),dyn_obj.worldCenter,1)
def jump(obj):
    dyn_obj = dynamic_objects[obj]
    force = dyn_obj.mass * jump / timeStep
    force /= float(jump_step)
    dyn_obj.ApplyForce(b2.Vec2(0,force),dyn_obj.worldCenter,True)
    
def add_static_box(pos,size,angle=0,data=0,sensor=False,body=None):
    global world,static_objects,index
    static_body = body
    if(static_body == None):
        pos_body = (pixel2meter(pos[0]), pixel2meter(pos[1]))
        if pybox2d:
            static_body = world.create_static_body(position=pos_body)
        else:
            static_body = world.CreateStaticBody(position=pos_body)
        
        
        static_body.angle = 0
    center_pos = (0,0)
    if body != None:
        center_pos = (pixel2meter(pos[0]),pixel2meter(pos[1]))
    polygon_shape = None

    if pybox2d:
        polygon_shape = b2.Polygon()
        polygon_shape.set_as_box(pixel2meter(size[0]), pixel2meter(size[1]),
                             center=center_pos)
        static_body.create_fixture(polygon_shape, sensor=sensor, user_data=data)
    else:
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(pixel2meter(size[0]), pixel2meter(size[1]),
                               b2Vec2(center_pos),angle)
        fixture_def = b2FixtureDef()
        fixture_def.density = 1
        fixture_def.shape = polygon_shape
        fixture_def.userData = data
        fixture_def.density = 1
        fixture_def.isSensor = sensor
        static_body.CreateFixture(fixture_def)
    
    if body == None:
        static_objects[index] = static_body
        index+=1
        return index - 1
    

def add_static_circle(pos,radius,sensor=False,user_data=0):
    static_body = world.CreateStaticBody(\
                                position=(pixel2meter(pos[0]), pixel2meter(pos[1])),\
                                shapes=b2.Circle(radius=pixel2meter(radius),)\
                                                     )
    static_objects[index] = static_body
    index+=1
    return index - 1
def remove_body(index):
    pass

