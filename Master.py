import socket
import threading

FLAGFORALGO=False

listIP = []
listPORT = []
listFD = []

def server():
    s = socket.socket()
    print("Socket successfully created")
    port = 8080
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', port))
    print("socket binded to %s" % (port))
    s.listen(5)
    print ("socket is listening")
    c, addr = s.accept()
    print('Got connection from', addr)
    listIP.append(addr[0])
    listFD.append(c)
    c.send(b'PORTNO')
    reply = c.recvfrom(1024)
    reply = reply[0].decode('utf-8').split()
    listPORT.append(int(reply[2]))
    print(listIP)
    print(listPORT)

flag=True
while(flag):
    print("::::::::::::::::::::::::MASTER::::::::::::::::::::::::::")
    print("Choose the following")
    print("1:Get a Node")
    print("2:Make a Ring")
    print("3:Run Algorithm")
    print("10: Exit")
    choice = input()
    if choice=='1':
        server()
    if choice=='2':
        if(len(listFD)>0):
            for i in range(len(listFD)):
                fd = listFD[i]
                if(i==(len(listFD)-1)):
                    msg = ('CONNECTCWTO 127.0.0.1 ' +str(listPORT[0])).encode('utf-8')
                else:
                    msg = ('CONNECTCWTO 127.0.0.1 '+str(listPORT[i+1])).encode('utf-8')
                fd.send(msg)
            for i in range(len(listFD)):
                fd = listFD[i]
                if(i==0):
                    msg = ('CONNECTACWTO 127.0.0.1 ' +str(listPORT[len(listFD)-1])).encode('utf-8')
                else:
                    msg = ('CONNECTACWTO 127.0.0.1 '+str(listPORT[i-1])).encode('utf-8')
                fd.send(msg)
            print("RING FORMED")
            FLAGFORALGO=True
        else:
            print("Cannot make ring without a node")

    if choice=='3':
        if FLAGFORALGO :
            print("RUN ALGORITHM HERE") # send msg to run algorithm
        else:
            print("Cannot Run Alorithm")
    if choice=='10':
        flag=False
