import socket
import select
# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 12345

# connect to the server on local computer
s.connect(('127.0.0.1', port))

# receive data from the server
#s.settimeout(2)

ready = select.select([s], [], [], 2)
if ready[0]:
    data = s.recv(4096)
else:
    data = "NOTHING"
print(data)
# close the connection
s.close()