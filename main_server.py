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
            print "LOOP"
            self.data = self.request.recv(1024).strip()
            split_request = self.data.split(';')
            #print split_request

            """Send a new id if not"""
            if split_request[0] == 'ID_REQUEST':
                client_id += 1
                self.request.sendall("NEW_ID;"+str(client_id))

            elif split_request[0] == 'SET_REQUEST':
                players_list[split_request[1]] = ";".join(split_request[1:])
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



if __name__ == "__main__":
    PORT = 12345
    HOST = "localhost"

    server = ThreadedTCPServer((HOST, PORT), KuduTCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    while 1:
        pass