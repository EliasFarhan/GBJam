'''
Created on 11 janv. 2014

@author: efarhan
'''

import json
from engine.const import log

def load_player(player):
    file = None
    try:
        file = open(player.filename, mode='r')
    except FileNotFoundError:
        return 2
    player_data = None
    try:
        player_data = json.loads(file.read())
    except ValueError: #No json object decoded
        return 3
    '''
    TODO: Create player instance
    
    '''
    player.pos = (player_data['pos'][0],player_data['pos'][1])
    player.size = (player_data['size'][0],player_data['size'][1])
    player.anim.path = player_data['path']
    player.anim.state_range = player_data['state_range']
    player.anim.path_list = player_data['path_list']
    
    file.close()
    return 1
def save_player(player):
    pass

def test():
    load_player("prout") #testing file not found error
    load_player("game_object.py") #testing JSON error

if __name__ == '__main__':
    test()
    
    