'''
Created on 11 dec. 2013

@author: efarhan
'''
import os
from os import listdir
from os.path import isfile, join
from engine.image_manager import load_image, get_size
from engine.const import CONST, log
from json_export.json_main import get_element
from engine.vector import Vector2


class Animation():
    def __init__(self,obj):
        self.obj = obj
        self.img = None
        self.path = ""
        self.state_range = {}
        self.path_list = []
        self.state = ""
        self.anim_counter = 0
        self.anim_freq = CONST.animation_step
        self.img_indexes = []
        self.index = 0

    def load_images(self,size=None,permanent = False):
        self.img_indexes = []
        
        for p in self.path_list:
            
            path = CONST.path_prefix+self.path+p
            files = []
            if ".png" in path:
                files = [path]
            else:
                files = [ os.path.join(path, f) for f in listdir(path) if (isfile(join(path, f)) and f.find(".png") != -1) ]
            files.sort()
            for f in files:
                self.img_indexes.append(load_image(f,permanent,prefix=False))
            try:
                self.img = self.img_indexes[0]
            except IndexError:
                pass
        if size is None:
            self.size = get_size(self.img)
        else:
            self.size = Vector2(size)
        if self.obj:
            self.obj.update_rect()

    def update_animation(self,state="",invert=False):
        if state != "":
            self.state = state
        if self.anim_counter == self.anim_freq:
            anim_index = []
            if self.state_range == {}:
                anim_index = self.img_indexes
            else:
                try:
                    anim_index = self.img_indexes[self.state_range[self.state][0]:self.state_range[self.state][1]]
                except KeyError:
                    return
            try:
                find_index = anim_index.index(self.img)
                if not invert:
                    if find_index == len(anim_index)-1:
                        self.index = 0
                    else:
                        self.index = find_index+1
                else:
                    if find_index == 0:
                        self.index = len(anim_index)-1

                    else:
                        self.index = find_index-1
                self.img = anim_index[self.index]
            except ValueError:
                try:
                    self.index = 0
                    self.img = anim_index[self.index]

                except IndexError:
                    pass
            self.anim_counter = 0
        else:
            self.anim_counter += 1

    @staticmethod
    def parse_animation(anim_data,obj=None):
        anim_type = get_element(anim_data,"anim_type")
        path = get_element(anim_data, "path")
        path_list = get_element(anim_data,"path_list")
        state_range = get_element(anim_data, "state_range")
        anim_freq = get_element(anim_data, "anim_freq")
        if not anim_freq:
            anim_freq = CONST.animation_step
        anim = None
        
        '''Check type entry is a string with '.' or alpha'''
        if anim_type and isinstance(anim_type, CONST.string_type):
            for c in anim_type:
                if c != '.' and c != '_' and not c.isalpha():
                    log("Error: Invalid character type for animation type: "+anim_type,1)
                    return None
        elif anim_type is None:
            anim_type = ''
        else:
            log("Error: Invalid type of anim_type, given: "+type(anim_type),1)
            return None
        if anim_type is not '':
            dir_list = anim_type.split(".")

            module_name = ".".join(dir_list[0:len(dir_list)-1])
            class_name = dir_list[len(dir_list)-1]
            log(module_name+" "+class_name)
            try:
                exec('''from %s import %s'''%(module_name, class_name ))
            except ImportError as e:
                log("Error while importing "+anim_type+" "+str(e), 1)
                return None
            
            try:
                d = locals()
                exec('''anim = %s(obj)'''% class_name, globals(), d)
                anim = d['anim']
            except Exception as e:
                log("Error initializing animation: "+str(e), 1)
                return None
        else:
            log("Use default animation")
            anim = Animation(obj)

        if anim and path:
            anim.path = path
        else:
            log("Error: UNDEFINED anim is None",1)
            return None
        if path_list and isinstance(path_list,list):
            anim.path_list = path_list
        if state_range and isinstance(state_range,dict):
            anim.state_range = state_range
        anim.anim_freq = anim_freq
        return anim
    def get_screen_pos(self):
        return (0,0)