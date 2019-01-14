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
Cmsg = 'NULL'
Smsg = 'NULL'
end = True
lockc = threading.Condition()
locks = threading.Condition()
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


def worker():
    global end
    global id
    global Cmsg
    global Smsg
    PhaseChange = 2
    phase = 0
    global s
    global c
    while(end):
        if PhaseChange == 2:
            print("PHASE ",phase)
            msgc = "clockwise " + str(id) + " "+str(2**phase)
            msga = "anticlockwise " + str(id) +" "+ str(2**phase)
            sendClient(msga)
            sendServer(msgc)
            phase = phase+1
            PhaseChange = 0
        #time.sleep(2)
        if s ==0 or c ==0:
            continue
        print("worker ")
        print("C M",Cmsg)
        print("S M",Smsg)
        if Cmsg != 'NULL' and Smsg != 'NULL':
            Cmsg = Cmsg.split()
            Smsg = Smsg.split()
            if len(Cmsg)>1 and len(Smsg)>1:
                if Cmsg[2]=='1' and Smsg[2]=='1':
                    maxVal =max(id,int(Cmsg[1]),int(Smsg[1]))
                    if(maxVal==int(Cmsg[1])):
                        sendClient(str(Cmsg[1]))
                    if(maxVal==int(Smsg[1])):
                        sendServer(str(Smsg[1]))
                if Cmsg[2]=='1' and Smsg[2]!='1':
                    pass
                if Cmsg[2]!='1' and Smsg[2]=='1':
                    pass
                if Cmsg[2]!='1' and Smsg[2]!='1':
                    if Cmsg[1] ==str(id) and Smsg[1]==str(id):
                        print("I am Leader")
                        end = False
                    else:
                        Cmsg[2] = str(int(Cmsg[2])-1)

        if Cmsg != 'NULL' and Smsg == 'NULL':
            print("C NN S N")
            Cmsg = Cmsg.split()
            if len(Cmsg)>1:
                if Cmsg[2]=='1':
                    if int(Cmsg[1])>id:
                        sendClient(str(Cmsg[1]))
                    if Cmsg[2]!='1':
                        Cmsg[2] = str(int(Cmsg[2])-1)
                        print("sent")
                        sendServer(' '.join(Cmsg))

            else:
                if Cmsg[0]!=str(id):
                    sendServer(Cmsg)

        if Cmsg == 'NULL' and Smsg != 'NULL':
            print("C N S NN")
            Smsg = Smsg.split()
            if len(Smsg)>1:
                if Smsg[2]=='1':
                    if int(Smsg[1])>id:
                        sendServer(str(Smsg[1]))
                    if Smsg[2]!='1':
                        Smsg[2] = str(int(Smsg[2])-1)
                        print("sent")
                        sendClient(' '.join(Smsg))
            else:
                if Smsg[0]!=str(id):
                    sendClient(Smsg)

        if Cmsg == 'NULL' and Smsg == 'NULL':
            pass

        if len(Cmsg)==1:
            if int(Cmsg[0]) != id :
                sendServer(str(Cmsg))
            else:
                PhaseChange = PhaseChange+1
        if len(Smsg)==1:
            if int(Smsg[0]) != id:
                sendClient(str(Cmsg))
            else:
                PhaseChange = PhaseChange + 1

        Cmsg='NULL'
        Smsg='NULL'
        c=0
        s=0
        print("worker unlocked")

def sendClient(msg):
    global CWFD
    CWFD.send(msg.encode('utf-8'))


def receiveClient():
    global CWFD
    global Cmsg
    global s
    global end
    while (end):
        ready = select.select([CWFD], [], [], 2)
        if ready[0]:
            msg = CWFD.recvfrom(1024)
            lockc.acquire()
            Cmsg = msg[0].decode('utf-8')
            s = 1
            lockc.release()
            print("received msg: ", Cmsg)
        else:
            lockc.acquire()
            Cmsg='NULL'
            s =1
            lockc.release()
        time.sleep(2)

def sendServer(msg):
    global SFD
    SFD.send(msg.encode('utf-8'))

def receiveServer():
    global SFD
    global Smsg
    global end
    global c
    while(end):
        ready = select.select([SFD], [], [], 2)
        if ready[0]:
            msg = SFD.recvfrom(1024)
            locks.acquire()
            Smsg = msg[0].decode('utf-8')
            c = 1
            locks.release()
            print("received msg: ",Smsg)
        else:
            locks.acquire()
            Smsg='NULL'
            c = 1
            locks.release()
        time.sleep(2)

PORT = 1025
t1 = threading.Thread(target=server)
t1.start()

t2 = threading.Thread(target=client)
t2.start()








