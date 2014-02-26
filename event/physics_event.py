'''
Created on Feb 26, 2014

@author: efarhan
'''

physics_events = []

def add_physics_event(event):
    global physics_events
    physics_events.append(event)
def get_physics_event():
    global physics_events
    return physics_events
def clear_physics_event():
    global physics_events
    del physics_events[:]

class PhysicsEvent:
    def __init__(self,a,b,begin):
        self.a=a
        self.b=b
        self.begin=begin

