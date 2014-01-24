'''
Created on Sep 9, 2013

@author: efarhan
'''

from engine.const import pybox2d,log
if pybox2d:
    import pypybox2d as b2
else:
    from Box2D import *
from engine.event import add_physics_event, PhysicsEvent

if pybox2d:
    class KuduContactListener(b2.contact_manager.ContactManager):
        def begin_contact(self, contact):
            a = contact._fixture_a.user_data
            b = contact._fixture_b.user_data
            add_physics_event(PhysicsEvent(a,b,True))
                
        def end_contact(self, contact):
            a = contact._fixture_a.user_data
            b = contact._fixture_b.user_data
            add_physics_event(PhysicsEvent(a,b,False))
else:
    class KuduContactListener(b2ContactListener):
        
        def BeginContact(self, contact):
            log("Begin contact")
            a = contact.fixtureA.userData
            b = contact.fixtureB.userData
            add_physics_event(PhysicsEvent(a,b,True))
        def EndContact(self, contact):
            a = contact.fixtureA.userData
            b = contact.fixtureB.userData
            add_physics_event(PhysicsEvent(a,b,False))