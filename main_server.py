import threading

__author__ = 'efarhan'

"""Must be run separately"""
import SocketServer


players_list = {}
client_id = 0


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class KuduTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global client_id
        # self.request is the TCP socket connected to the client
        while(1):
            self.data = self.request.recv(1024).strip()
            split_request = self.data.split(';')
            #print split_request

            """Send a new id if not"""
            if split_request[0] == 'ID_REQUEST':
                client_id += 1
                self.request.sendall("NEW_ID;"+str(client_id))

            elif split_request[0] == 'SET_REQUEST':
                players_list[int(split_request[1])] = ";".join(split_request[1:])
                self.request.sendall("SET_OK")
            elif split_request[0] == 'GET_REQUEST':
                """Return all content of players"""
                self.request.sendall("REQUEST;"+str(len(players_list.keys()))+";")
                self.request.recv(1024)
                for p in players_list.keys():
                    self.request.sendall(players_list[p]+";")
                    self.request.recv(1024)
            else:
                self.request.sendall("ERROR;BAD_REQUEST")

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

class KuduUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        socket = self.request[1]
        player_id = int((self.request[0].strip()).split(";")[1])
        while(1):
            for p in players_list.keys():
                if p != player_id:
                    print "YOLO", player_id, self.client_address
                    socket.sendto(players_list[p]+";", self.client_address)



if __name__ == "__main__":
    PORT = 12345
    HOST = "localhost"

    server = ThreadedTCPServer((HOST, PORT), KuduTCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    update_server = ThreadedUDPServer((HOST, PORT+1), KuduUDPHandler)
    update_thread = threading.Thread(target=update_server.serve_forever)
    update_thread.daemon = True
    update_thread.start()
    while 1:
        pass