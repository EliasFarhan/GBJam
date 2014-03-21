'''
Created on Mar 21, 2014

@author: elias
'''
import math
from numbers import Number

class Matrix22():
    def __init__(self,values):
        self.values = values
    def __mul__(self,vector):
        return (self.values[0][0]*vector.x+self.values[0][1]*vector.y,
                self.values[1][0]*vector.x+self.values[1][1]*vector.y)
class Vector2():
    def __init__(self):
        self.length = 1.0
        self.x = 1.0
        self.y = 0.0
    def coordinate(self,x,y):
        self.x = x
        self.y = y
        self.length = math.sqrt(x**2+y**2)
        return self
    def orientation(self,length,angle):
        self.x = length*math.cos(angle*math.pi/180)
        self.y = length*math.sin(angle*math.pi/180)
        self.length = length
        return self
    def tuple2(self,tuple):
        if not tuple:
            return None
        self.coordinate(tuple[0], tuple[1])
        return self
    
    def rotate(self,angle):
        (self.x,self.y) = Matrix22([[math.cos(angle*math.pi/180),-math.sin(angle*math.pi/180)],[math.sin(angle*math.pi/180),math.cos(angle*math.pi/180)]])*(self)
    def __add__(self,v):
        return Vector2().coordinate(self.x+v.x, self.y+v.y)
    def __sub__(self,v):
        return Vector2().coordinate(self.x-v.x, self.y-v.y)
    def __mul__(self,v):
        if v.__class__ == Vector2:
            return Vector2().coordinate(self.x*v.x, self.y*v.y)
        elif isinstance(v, Number):
            return Vector2().coordinate(self.x*v, self.y*v)
        else:
            raise TypeError("Vector can only multiply numbers or Vector, type given: %s"%(str(type(v))))
        return None
    def __div__(self,v):
        if v.__class__ == Vector2:
            return Vector2().coordinate(self.x/v.x, self.y/v.y)
        elif isinstance(v, Number):
            return Vector2().coordinate(self.x/v, self.y/v)
        else:
            raise TypeError("Vector can only divide numbers or Vector, type given: %s"%(str(type(v))))
        return None
    def dot(self,v):
        return self.x*v.x+self.y*v.y
    def get_tuple(self):
        return (self.x,self.y)
    def get_int_tuple(self):
        return (int(self.x),int(self.y))