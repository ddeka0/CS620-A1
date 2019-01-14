import socket
import threading
import random
import os
import time
import select


id = os.getpid()
print("NODE ID: ",id)

c=0
s=0
PORT = 1205
CWFD = ''
SFD = ''
flag = 0
phase = 1
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
                t3 = threading.Thread(target=transition)
                t3.start()
            if fromMaster[0] == 'EXIT':
                s.close()
        except IndexError:
            print("DONE: SUCCESS")
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
    global end
    global flag
    msgc = "clockwise " + str(id) + " 1 "
    msga = "anticlockwise " + str(id) + " 1 "
    sendClient(msga)
    sendServer(msgc)
    while(end):
        time.sleep(1)
        receiveClient()
        time.sleep(1)
        receiveServer()
        time.sleep(1)
        worker()
        time.sleep(5)





def worker():
    print("in worker")
    global Smsg
    global Cmsg
    global id
    global phase
    Smsg = Smsg.split()
    Cmsg = Cmsg.split()
    if Smsg[0]=='NULL' and Cmsg[0]=='NULL':
        Smsg='NULL'
        Cmsg='NULL'
        return
    else:
        print(Cmsg)
        print(Smsg)
        if len(Smsg)==3 and len(Cmsg)==3:
            if Smsg[2]=="1" and Cmsg[2]=='1':
                if id != int(Smsg[1]) and id != int(Cmsg[1]):
                    retval = max(id,int(Smsg[1]),int(Cmsg[1]))
                    if retval == int(Smsg[1]):
                        sendServer(Smsg[1])
                    if retval == int(Cmsg[1]):
                        sendClient((Cmsg[1]))
                if int(Smsg[1])==id and int(Cmsg[1])==id:
                        print("I am leader")
                        end = False
            if Smsg[2]=='1' and Cmsg[2]!='1':
                pass
            if Smsg[2] != '1' and Cmsg[2] == '1':
                pass
            if Smsg[2] != "1" and Cmsg[2] != '1':
                if (id == int((Cmsg[1]))) and (id == int((Smsg[1]))):
                    print("I am leader")
                    end = False
                if (id != int((Cmsg[1]))) and (id != int((Smsg[1]))):
                    Cmsg[2] = str(int(Cmsg[2])-1)
                    Smsg[2] = str(int(Smsg[2])-1)
                    sendClient(' '.join(Smsg))
                    sendServer(' '.join(Cmsg))

        if len(Smsg)==1 and len(Cmsg)==1 and Smsg[0]!='NULL' and Cmsg[0]!='NULL':
            if int(Smsg[0])==id and int(Cmsg[0])==id:
                msgc = "clockwise " + str(id) + " "+str(pow(2,phase))+' '
                msga = "anticlockwise " + str(id) + " "+str(pow(2,phase))+' '
                sendClient(msga)
                sendServer(msgc)
                phase = phase+1
            if int(Cmsg[0]) != id and int(Smsg[0]) != id:
                sendServer(Cmsg[0])
                sendClient(Smsg[0])
        if Smsg[0]=='NULL' and len(Cmsg)==3:
            if Cmsg[2]=='1':
                retval = max(id,int(Cmsg[1]))
                if retval == int(Cmsg[1]):
                    sendClient(Cmsg[1])
            else:
                Cmsg[2] = str(int(Cmsg[2])-1)
                sendServer(' '.join(Cmsg))

        if Cmsg[0] == 'NULL' and len(Smsg)==3:
            if Smsg[2] == '1':
                retval = max(id, int(Smsg[1]))
                if retval == int(Smsg[1]):
                    sendServer(Smsg[1])
            else:
                Smsg[2] = str(int(Smsg[2]) - 1)
                sendClient(' '.join(Smsg))

        if Smsg[0]=='NULL' and len(Cmsg)==1:
            if int(Cmsg[0])!=id:
                sendServer(Cmsg[0])

        if Cmsg[0] == 'NULL' and len(Smsg)==1:
            if int(Smsg[0])!=id:
                sendClient(Smsg[0])

    Smsg = 'NULL'
    Cmsg = 'NULL'
    print("end worker")


def sendClient(msg):
    global CWFD
    CWFD.send(msg.encode('utf-8'))


def receiveClient():
    global CWFD
    global Cmsg
    result = select.select([CWFD], [], [], 0)
    if result[0]:
        msg = CWFD.recv(1024)
        msg = msg.decode('utf-8')
        print("received msg:", msg)
        Cmsg = msg

def sendServer(msg):
    global SFD
    SFD.send(msg.encode('utf-8'))

def receiveServer():
    global SFD
    global Smsg
    result = select.select([SFD], [], [], 0)
    if result[0]:
        msg = SFD.recv(1024)
        msg = msg.decode('utf-8')
        print("received msg:", msg)
        Smsg = msg

PORT = 1025
t1 = threading.Thread(target=server)
t1.start()

t2 = threading.Thread(target=client)
t2.start()








