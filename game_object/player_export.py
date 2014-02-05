'''
Created on 11 janv. 2014

@author: efarhan
'''

import json
from engine.const import log
from physics.physics import add_dynamic_object, add_static_box
from engine.init import get_screen_size
from engine.event import add_button

def load_player(player):
    file = None
    try:
        file = open(player.filename, mode='r')
    except IOError:
        return 2
    player_data = None
    try:
        player_data = json.loads(file.read())
    except ValueError: #No json object decoded
        return 3
    '''
    Create player instance
    
    '''
    player.pos = (player_data['pos'][0][0],player_data['pos'][1][0])
    player.screen_relative_pos = (player_data['pos'][0][1],player_data['pos'][1][1])
    player.size = (player_data['size'][0],player_data['size'][1])
    player.anim.path = player_data['path']
    player.anim.state_range = player_data['state_range']
    player.anim.path_list = player_data['path_list']
    
    
    physics_pos = (player.pos[0]+player.screen_relative_pos[0]*get_screen_size()[0],
                   player.pos[1]+player.screen_relative_pos[1]*get_screen_size()[1])
    player.body = add_dynamic_object(player,physics_pos)
    for physic_object in player_data['physic_objects']:
        pos = physic_object['pos']
        size = physic_object['size']
        angle = physic_object['angle']
        data = physic_object['user_data']
        sensor = physic_object['sensor']
        add_static_box(pos, size, angle, data, sensor, body=player.body)
    for player_action in player_data['player_actions'].items():
        add_button(player_action[0],player_action[1])
    log(player.body.position)
    file.close()
    return 1

def save_player(player):
    pass
    
    