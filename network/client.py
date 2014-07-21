import socket
from threading import Lock, Thread
from engine.const import log, CONST
from engine.vector import Vector2



players = {}

PORT = CONST.port
HOST = CONST.host


update_thread = None
self_id = 0
sock = None

def get_self_id():
    global self_id
    return self_id


def init():
    global update_thread, self_id,sock
    data = "ID_REQUEST;"
    new_id_request = None

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall(data)
        new_id_request = sock.recv(1024)
    except socket.error as e:
        sock.close()
        sock = None
        log("Network init: "+str(e),1)
        return

    self_id = new_id_request.split(";")[1]


def set_request(pos, state, frame):
    global sock
    """Change the position of the player on the server"""

    """Set correct pos, state, frame"""
    try:
        if not sock:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
        sock.sendall("SET_REQUEST;"+str(self_id)+";"+pos.get_string() +";"+state+";"+str(frame)+";")
        sock.recv(1024)
    except socket.error as e:
        sock.close()
        sock = None
        log("Network set: "+str(e),1)
        return

def get_players_request():
    global sock
    try:
        if not sock:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
        sock.sendall("GET_REQUEST;")
        get_request_nmb = sock.recv(1024)
        #log(get_request_nmb)
        try:
            nmb = int(get_request_nmb.split(';')[1])
            sock.sendall("%i;"%nmb)

            length = 5
            for i in range(nmb):
                get_request_data = sock.recv(1024)
                #log(get_request_data)
                """Position"""
                parsed_data = get_request_data.split(';')
                parsed_data[1] = parsed_data[1].split(',')
                parsed_data[1] = Vector2(int(float(parsed_data[1][0])), int(float(parsed_data[1][1])))
                """Frame"""
                parsed_data[3] = int(parsed_data[3])

                """update players position"""
                players[parsed_data[0]] = parsed_data
                sock.sendall("NEXT")
        except IndexError:
            pass
    except socket.error as e:
        sock.close()
        sock = None
        log("Network get: "+str(e),1)
        return


