'''
Created on 17 mars 2014

@author: efarhan
'''
from animation.animation_main import Animation

class ObjectAnimation(Animation):
    '''Animation for an object with physics body'''
    def __init__(self,obj):
        Animation.__init__(self)
        self.obj = obj
    def load_images(self, size=None, permanent=False):
        Animation.load_images(self, size=size, permanent=permanent)
    def update_animation(self, state="", invert=False):
        return Animation.update_animation(self, state=state, invert=invert)
    def update_pos(self):
        pass
        