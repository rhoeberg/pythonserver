import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

def printByte(data):
    print(data.decode("utf-8"))

def sendToAddr(msg, addr):
    msg = msg.encode("utf-8")
    sent = sock.sendto(msg, addr)

def waitForSyn():
    data, addr = sock.recvfrom(4096)
    printByte(data)
    sendToAddr("com-0 accept " + str(server_address[0]), addr)
    print("waiting for ack")
    data, addr = sock.recvfrom(4096)
    printByte(data)

def recMsg():
    data, addr = sock.recvfrom(4096)
    i = int(data.decode("utf-8").split(' ')[0][4:]) + 1
    printByte(data)
    return i, addr

def sendRes(i, addr):
    sendToAddr("res-" + str(i) + " I am server", addr)
    
while True:
    waitForSyn()
    while True:
        i, addr = recMsg()
        sendRes(i, addr)
    
