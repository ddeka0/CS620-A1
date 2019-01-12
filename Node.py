import socket
import threading
import random

PORT = 1205
CWFD = ' '    #clockWise FD
ACWFD = ' '   #Anti clockwise FD
def server():
    s = socket.socket()
    print("Socket successfully created")
    global PORT

    a = True

    while(a):
        try:
            s.bind(('127.0.0.1', PORT))
            a = False
        except OSError:
            PORT = random.randint(1026, 50000)

    print("socket binded to %s" % (PORT))

    s.listen(5)
    print ("socket is listening")
    while True:
        # Establish connection with client.
        c, addr = s.accept()
        print('Got connection from', addr)
        # send a thank you message to the client.
        c.send(b'Thank you for connecting')
        # Close the connection with the client
        c.close()

def client():
    global PORT
    Flag = True
    s = socket.socket()
    port = 8080
    s.connect(('127.0.0.1', port))
    while(Flag):
        fromMaster = ((s.recv(1024)).decode('utf-8')).split()
        try:
            if fromMaster[0] == 'PORTNO':
                reply = 'PORT NO: ' + str(PORT)
                reply = reply.encode('utf-8')
                s.send(reply)
            if fromMaster[0] == 'CONNECTCWTO':
                clientCW(fromMaster)
            if fromMaster[0] == 'CONNECTACWTO':
                clientACW(fromMaster)
            if fromMaster[0] == 'EXIT':
                s.close()
        except IndexError:
            print("Master Died: TRY AGAIN")
            break

def clientCW(fromMaster):
    CWFD = socket.socket()
    IP = fromMaster[1]
    PORT = int(fromMaster[2])
    CWFD.connect((IP,PORT))
    print("connected to ",IP , PORT)


def clientACW(fromMaster):
    ACWFD = socket.socket()
    IP = fromMaster[1]
    PORT = int(fromMaster[2])
    ACWFD.connect((IP,PORT))
    print("connected to ",IP , PORT)


PORT = 1025
t1 = threading.Thread(target=server)
t1.start()

t2 = threading.Thread(target=client)
t2.start()




