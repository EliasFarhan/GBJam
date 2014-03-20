'''
Created on 11 dec. 2013

@author: efarhan
'''
import os
from os import listdir
from os.path import isfile, join
from engine.image_manager import load_image, load_image_with_size, get_size
from engine.const import animation_step,path_prefix, log
from json_export.json_main import get_element

class Animation():
    def __init__(self,obj):
        self.obj = obj
        self.img = 0
        self.path = ""
        self.state_range = {}
        self.path_list = []
        self.state = ""
        self.anim_counter = 0
        self.anim_freq = animation_step
        self.img_indexes = []
    def load_images(self,size=None,permanent = False):
        self.img_indexes = []
        
        for p in self.path_list:
            
            path = path_prefix+self.path+p
            files = []
            if ".png" in path:
                files = [path]
            else:
                files = [ os.path.join(path, f) for f in listdir(path) if (isfile(join(path, f)) and f.find(".png") != -1) ]
            files.sort()
            for f in files:
                if size == None:
                    self.img_indexes.append(load_image(f,permanent))
                else:
                    self.img_indexes.append(load_image_with_size(f, size, permanent))
            self.img = self.img_indexes[0]
        self.size = get_size(self.img)
        if self.obj:
            self.obj.update_rect()
    def update_animation(self,state="",invert=False):
        if state != "":
            self.state = state
        if(self.anim_counter == self.anim_freq):
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
                        self.img = anim_index[0]
                    else:
                        self.img = anim_index[find_index+1]
                else:
                    if find_index == 0:
                        self.img = anim_index[len(anim_index)-1]
                    else:
                        self.img = anim_index[find_index-1]
            except ValueError:
                try:
                    self.img = anim_index[0]
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
            anim_freq = animation_step
        anim = None
        
        '''Check type entry is a string with '.' or alpha'''
        if anim_type and type(anim_type) == str:
            for c in anim_type:
                if c != '.' and not c.isalpha():
                    return None
        if anim_type != '':
            dir_list = anim_type.split(".")
            
            try:
                exec('''from %s import %s'''%(".".join(dir_list[0:len(dir_list)-1]), dir_list[len(dir_list)-1]))
            except ImportError as e:
                log("Error while importing "+anim_type+" "+str(e), 1)
                return None
            
            try:
                exec('''anim = %s(obj)'''%(dir_list[len(dir_list)-1]))
            except Exception as e:
                log("Error initializing animation: "+str(e),1)
                return None
        else:
            anim = Animation(obj)
        if path:
            anim.path = path
        else:
            return None
        if path_list and type(path_list) == list:
            anim.path_list = path_list
        if state_range and type(state_range) == dict:
            anim.state_range = state_range
        anim.anim_freq = anim_freq
        return anim