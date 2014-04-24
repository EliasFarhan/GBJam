import socket
from threading import Lock, Thread
from engine.const import log
from engine.vector import Vector2



players = {}

PORT = 9999
HOST = "92.222.15.13"


update_thread = None
self_id = 0


def get_self_id():
    global self_id
    return self_id


def init():
    global update_thread, self_id
    data = "ID_REQUEST;"
    new_id_request = None

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall(data)
        new_id_request = sock.recv(1024)
    finally:
        sock.close()
    self_id = new_id_request.split(";")[1]


def set_request(pos, state, frame):
    """Change the position of the player on the server"""

    """Set correct pos, state, frame"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall("SET_REQUEST;"+str(self_id)+";"+pos.get_string() +";"+state+";"+str(frame)+";")
        new_id_request = sock.recv(1024)
    finally:
        sock.close()


def get_players_request():
    global sock
    log("GET_REQUEST")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall("GET_REQUEST;")
        get_request_data = sock.recv(1024)
        print get_request_data
        try:
            nmb = int(get_request_data.split(';')[1])
            length = 5
            for i in range(nmb):
                """Position"""
                parsed_data = get_request_data.split(';')[length*i+2:length*i+7]
                print parsed_data
                parsed_data[1] = parsed_data[1].split(',')
                parsed_data[1] = Vector2(int(float(parsed_data[1][0])), int(float(parsed_data[1][1])))
                """Frame"""
                parsed_data[3] = int(parsed_data[3])

                """update players position"""
                players[parsed_data[0]] = parsed_data[1:]
        except IndexError:
            pass
    finally:
        sock.close()



