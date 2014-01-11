'''
Created on 11 janv. 2014

@author: efarhan
'''

import json

def load_player(filename):
    file = None
    try:
        file = open(filename, mode='r')
    except FileNotFoundError:
        return False
    player_data = None
    try:
        player_data = json.loads(file.read())
    except ValueError: #No json object decoded
        return False
    '''
    TODO: Create player instance
    
    '''
    
    file.close()
def save_player(player):
    pass

def test():
    load_player("prout") #testing file not found error
    load_player("game_object.py") #testing JSON error

if __name__ == '__main__':
    test()
    
    