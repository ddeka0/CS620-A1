# Import socket module
import socket

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 8080

# connect to the server on local computer
s.connect(('127.0.0.1', port))

# receive data from the server
print(s.recv(1024))
reply = 'PORT NO: '+str(1234)
reply = reply.encode('utf-8')
s.send(reply)
# close the connection
s.close()