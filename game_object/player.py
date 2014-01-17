'''
Created on 8 sept. 2013

@author: efarhan
'''
from game_object.image import Image
from engine.json_export import json_player_import, json_player_export

class Player(Image):
    def __init__(self, json_path):
        '''Parse json file'''
        self.json_path = json_path
        json_player_import(self)
        
    def loop(self, screen, screen_pos):
        self.update_event()
        Image.loop(self, screen, screen_pos)
    
    def init_physics(self):
        '''Used during json parsing
        '''
        pass
    def update_event(self):
        '''Taking events from event.py:
        -Physics events
        -Input events
        -Others events
        
        And transform player attributes:
        -Animation state 
        -Position
        -Size'''
        pass
    def save(self):
        '''Save the player into the JSON file'''
        json_player_export(self)
    