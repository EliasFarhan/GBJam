'''
Created on Mar 21, 2014

@author: elias
'''
import math
import sys
import traceback
from numbers import Number
from engine.const import log


class Matrix22():
    def __init__(self,values):
        self.values = values
    def __mul__(self,vector):
        return (self.values[0][0]*vector.x+self.values[0][1]*vector.y,
                self.values[1][0]*vector.x+self.values[1][1]*vector.y)
class Vector2():
    def __init__(self,*args):
        '''try:
    iterator = iter(theElement)
except TypeError:
    # not iterable
else:
    # iterable'''
        try:
            self.x = 0.0
            self.y = 0.0
            self.length = 0.0
            if len(args) == 2:
                self.x = args[0]
                self.y = args[1]
            elif len(args) == 1:
                self.x = args[0][0]
                self.y = args[0][1]

            self.length = math.sqrt(self.x**2+self.y**2)
        except TypeError as e:
            log("Error: Vector2 invalid arg type with: "+str(args)+ "|"+str(e), 1)
            ex_type, ex, tb = sys.exc_info()
            traceback.print_tb(tb)
        except IndexError as e:
            log("Error: Vector2 with argument: "+str(args)+ "|"+str(e), 1)
            ex_type, ex, tb = sys.exc_info()
            traceback.print_tb(tb)
        except AttributeError as e:
            log("Error: Vector2 with attribute error: "+str(args)+ "|"+str(e), 1)
            ex_type, ex, tb = sys.exc_info()
            traceback.print_tb(tb)

    def orientation(self,length,angle):
        self.x = length*math.cos(angle*math.pi/180)
        self.y = length*math.sin(angle*math.pi/180)
        self.length = length
        return self
    def normalize(self):
        try:
            ratio = 1.0/self.length
            self.x *= ratio
            self.y *= ratio
            self.length = 1.0
        except ZeroDivisionError:
            pass
    def invert(self):
        return Vector2(self.y, self.x)

    
    def rotate(self,angle):
        (self.x,self.y) = Matrix22([[math.cos(angle*math.pi/180),-math.sin(angle*math.pi/180)],[math.sin(angle*math.pi/180),math.cos(angle*math.pi/180)]])*(self)
    def __add__(self,v):
        return Vector2(self.x+v.x, self.y+v.y)
    def __sub__(self,v):
        return Vector2(self.x-v.x, self.y-v.y)
    def __mul__(self,v):
        if v.__class__ == Vector2:
            return Vector2(self.x*v.x, self.y*v.y)
        elif isinstance(v, Number):
            return Vector2(self.x*v, self.y*v)
        else:
            raise TypeError("Vector can only multiply numbers or Vector, type given: %s"%(str(type(v))))
        return None
    def __div__(self,v):
        try:
            if v.__class__ == Vector2:
                return Vector2(self.x/v.x, self.y/v.y)
            elif isinstance(v, Number):
                return Vector2(self.x/v, self.y/v)
            else:
                raise TypeError("Vector can only divide numbers or Vector, type given: %s"%(str(type(v))))
            return None
        except ZeroDivisionError:
            log("Error: Division by zero with: "+str(self.get_tuple())+", "+str(v.get_tuple()),1)
            return None
    def dot(self,v):
        return self.x*v.x+self.y*v.y
    def get_tuple(self):
        return self.x,self.y
    def get_int_tuple(self):
        return int(self.x),int(self.y)