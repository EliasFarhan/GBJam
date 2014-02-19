'''
Created on Feb 19, 2014

@author: efarhan
'''
from engine.const import log
import json

def load_json(filename):
    file = None
    try:
        file = open(filename, mode='r')
        
    except IOError:
        log("Loading file error: "+filename,1)
        return False
    json_data = None
    try:
        json_data = json.loads(file.read())
    except ValueError as e: #No json object decoded
        log(e)
        return False
    file.close()
    return json_data