
from engine.const import move_speed, jump, framerate,jump_step,gravity, log,\
    pybox2d, pookoo
if pookoo:
    import physics
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
    
    world = b2World(gravity=(0,gravity_value))
    world.contactListener = KuduContactListener()

def add_dynamic_object(obj,pos):
    global world
    position = (pixel2meter(pos[0]),pixel2meter(pos[1]))
    dynamic_object = world.CreateDynamicBody(position=position)
    dynamic_object.angle = 0
    dynamic_object.fixed_rotation = True
    return dynamic_object

def remove_body(index):
    global world
    try:
        world.DestroyBody(static_objects.pop(index))
    except KeyError:
        pass
def update_physics():
    global timeStep, vel_iters, pos_iters
    world.Step(timeStep,vel_iters,pos_iters)
    world.ClearForces()
    
def move(body,vx=None,vy=None):
    dyn_obj = body
    velx,vely = dyn_obj.linearVelocity.x,dyn_obj.linearVelocity.y
    fx,fy=0,0
    if(vx != None):
        velx = vx * move_speed - velx
        fx = dyn_obj.mass * velx / timeStep
    if(vy != None):
        vely = vy * move_speed - vely
        fy = dyn_obj.mass * vely / timeStep
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
        static_body = world.CreateStaticBody(position=pos_body)
        static_body.angle = 0
    center_pos = (0,0)
    if body != None:
        center_pos = (pixel2meter(pos[0]),pixel2meter(pos[1]))
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


