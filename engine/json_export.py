'''
Created on Jan 13, 2014

@author: efarhan
'''

import json

def save_file(filename,data_content):
    file = None
    try:
        file = open(filename,mode='w')
    except FileNotFoundError:
        return False
    file.write(data_content)
    file.close()



def load_file(filename,data_container):
    file = None
    try:
        file = open(filename, mode='r')
    except FileNotFoundError:
        return False
    try:
        data_container = json.loads(file.read())
    except ValueError: #No json object decoded
        file.close()
        return False
    file.close()
    return True

def json_player_import(player):
    player_data = None
    if load_file(player.json_path,player_data):
        player.pos = (player_data['pos'][0],player_data['pos'][1])
        player.anim.path = player_data['path']
        player.anim.path_list = player_data['path_list']
        player.anim.range_state = player_data['range_state']
        '''Import player:
        -path_list
        -pos
        -size
        etc...'''
        pass
def json_player_export(player):
    pass

def json_level_import(gamestate):
    
    ''' 
    TODO: Import a level with:
    
    -Physics static object
    -Images with or without animation
    -IA (if any)
    -Player position, size, etc... but not recreate the player!!!
    '''
    pass
