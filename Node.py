import socket
import threading
import random
import os

id = os.getpid()

PORT = 1205
CWFD = ''
SFD = ''
Cmsg = 'NULL'
Smsg = 'NULL'
end = True
lock = threading.Condition()
def server():
    global SFD
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
    SFD, addr = s.accept()
    print('Got connection from', addr)


def client():
    global PORT
    Flag = True
    global end
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
            if fromMaster[0] == 'START':
                transition()
            if fromMaster[0] == 'EXIT':
                s.close()
        except IndexError:
            print("Master Died: TRY AGAIN")
            end = False
            break

def clientCW(fromMaster):
    global CWFD
    CWFD = socket.socket()
    IP = fromMaster[1]
    PORT = int(fromMaster[2])
    CWFD.connect((IP,PORT))
    print("connected to ",IP , PORT)

def transition():
    t5 = threading.Thread(target=receiveServer)
    t6 = threading.Thread(target=receiveClient)
    t3 = threading.Thread(target=worker)
    t3.start()
    t5.start()
    t6.start()
    msgc = "clockwise " + str(id) + " 1"
    msga = "anticlockwise " + str(id) + " 1"
    sendClient(msga)
    sendServer(msgc)

def worker():
    pass


def sendClient(msg):
    global CWFD
    CWFD.send(msg.encode('utf-8'))


def receiveClient():
    global CWFD
    global Cmsg
    while (end):
        msg = CWFD.recvfrom(1024)
        lock.acquire()
        Cmsg = msg[0].decode('utf-8')
        lock.notify()
        lock.release()
        print("received msg: ", Cmsg)

def sendServer(msg):
    global SFD
    SFD.send(msg.encode('utf-8'))

def receiveServer():
    global SFD
    global Smsg
    global end
    while(end):
        msg = SFD.recvfrom(1024)
        lock.acquire()
        Smsg = msg[0].decode('utf-8')
        lock.notify()
        lock.release()
        print("received msg: ",Smsg)


PORT = 1025
t1 = threading.Thread(target=server)
t1.start()

t2 = threading.Thread(target=client)
t2.start()








