import socket
import threading

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
    c.send(b'PORT NO')
    reply = c.recvfrom(1024)
    reply = reply[0].decode('utf-8').split()
    listPORT.append(int(reply[2]))
    print(listIP)
    print(listPORT)
    c.close()

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
        pass
    if choice=='3':
        pass
    if choice=='10':
        flag=False
