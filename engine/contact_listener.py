"""
Should be put in physics

Created on Sep 9, 2013

@author: efarhan
"""
from engine.const import pookoo
if not pookoo:
    from Box2D import *
from engine.event import add_physics_event, PhysicsEvent
if not pookoo:
    class KuduContactListener(b2ContactListener):
        def BeginContact(self, contact):
            a = contact.fixtureA.userData
            b = contact.fixtureB.userData
            add_physics_event(PhysicsEvent(a,b,True))
        def EndContact(self, contact):
            a = contact.fixtureA.userData
            b = contact.fixtureB.userData
            add_physics_event(PhysicsEvent(a,b,False))
