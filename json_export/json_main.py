'''
Created on Feb 19, 2014

@author: efarhan
'''

import json

def get_element(data_dict,name):
    try:
        return data_dict[name]
    except KeyError:
        return None
    

def load_json(filename):
    '''Load a JSON file
    
    Return None if IOError or ValueError and add an error in the stderr 
    '''
    file = None
    try:
        file = open(filename, mode='r')
        
    except IOError:
        from engine.const import log
        log("Loading file error: "+filename,1)
        return None
    json_data = None
    try:
        json_data = json.loads(file.read())
    except ValueError as e: #No json object decoded
        from engine.const import log
        log(e,1)
        return None
    file.close()
    return json_data