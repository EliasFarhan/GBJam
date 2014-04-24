import socket
from threading import Lock, Thread
from engine.vector import Vector2


class SharedData():
    def __init__(self,data):
        self.data = data
        self.lock = Lock()

    def access_data(self):
        """Always free the shared data after being used"""
        self.lock.acquire()
        return self.data

    def free_data(self):
        self.lock.release()

players_list = SharedData({})


class PlayersListUpdate(Thread):
    def run(self):
        self.finish = False
        while not self.finish:
            sock = shared_socket.access_data()
            players_data = sock.recv(1024)
            shared_socket.free_data()
            sock = None
            parsed_data = players_data.split(";")
            if parsed_data[0] != "NEW_ID":
                """Position"""
                parsed_data[1] = parsed_data[1].split(',')
                parsed_data[1] = Vector2(int(parsed_data[1][0]),int(parsed_data[1][1]))
                """Frame"""
                parsed_data[3] = int(parsed_data[3])

                """update players position"""
                players = players_list.access_data()
                players[parsed_data[0]] = parsed_data[1:]
                players_list.free_data()

    def finish(self):
        self.finish = True

HOST, PORT = "eliasfarhan.ch", 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
shared_socket = SharedData(client_socket)
update_thread = None
self_id = 0


def get_self_id():
    global self_id
    return self_id


def init():
    global update_thread,self_id
    sock = shared_socket.access_data()
    sock.sendto("ID_REQUEST;", (HOST, PORT))
    new_id_request = sock.recv(1024)
    shared_socket.free_data()
    sock = None
    self_id = new_id_request.split(";")[1]
    '''
    run thread getting new players position
    '''
    update_thread = PlayersListUpdate()
    update_thread.daemon = True
    update_thread.start()


def set_request(pos, state, frame):
    """Change the position of the player on the server"""

    """Set correct pos, state, frame"""
    sock = shared_socket.access_data()
    sock.sendto("SET_REQUEST;"+str(self_id)+";"+pos.get_string() +";"+state+";"+str(frame)+";", (HOST, PORT))
    shared_socket.free_data()
    sock = None


def exit_network():
    global update_thread
    update_thread.finish()


def get_players_request():
    sock = shared_socket.access_data()
    sock.sendto("GET_REQUEST;", (HOST, PORT))
    shared_socket.free_data()
    sock = None


