# coding=utf-8
import sfml as sf
# --- the client ---
# create a socket and connect it to 192.168.1.50 on port 55001
socket = sf.TcpSocket()
socket.connect(sf.IpAddress.from_string("92.222.15.13"), 55001)


# send a message to the connected host
message = u"Hello World".encode('utf-8')
socket.send(message)

# receive an answer from the server
answer = socket.receive(1024)
print("The server said: {0}".format(answer))
