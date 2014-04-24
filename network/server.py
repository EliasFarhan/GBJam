import SocketServer

"""
Protocol instructions:
-REQUEST_ID (return a unique id for the client)
"""

client_id = 0


class KuduUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        global client_id
        data = self.request[0].strip()
        socket = self.request[1]
        print "{} wrote:".format(self.client_address[0])
        print data

        if data == 'ID_REQUEST':
            client_id += 1
            socket.sendto("NEW_ID;"+str(client_id), self.client_address)
        else:
            socket.sendto("ERROR;BAD_REQUEST", self.client_address)


if __name__ == "__main__":
    HOST, PORT = "92.222.15.13", 9999
    server = SocketServer.UDPServer((HOST, PORT), KuduUDPHandler)
    server.serve_forever()