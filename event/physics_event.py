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
    result = []
    for i in range(len(physics_events)):
        result.append(physics_events.pop())
    return result


class PhysicsEvent:
    def __init__(self,a,b,begin):
        self.a=a
        self.b=b
        self.begin=begin

