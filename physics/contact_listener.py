'''
Created on Sep 9, 2013

@author: efarhan
'''
import engine
import pypybox2d as b2
from engine.event import add_physics_event, PhysicsEvent

class KuduContactListener(b2.contact_manager.ContactManager):
    def begin_contact(self, contact):
        a = contact._fixture_a.user_data
        b = contact._fixture_b.user_data
        add_physics_event(PhysicsEvent(a,b,True))
            
    def end_contact(self, contact):
        a = contact._fixture_a.user_data
        b = contact._fixture_b.user_data
        add_physics_event(PhysicsEvent(a,b,False))
