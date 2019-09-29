import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
connected = False
conAddr = None

def printByte(data):
    print(data.decode("utf-8"))

def sendToAddr(msg, addr):
    msg = msg.encode("utf-8")
    sent = sock.sendto(msg, addr)

def waitForSyn():
    sock.setblocking(True)
    data, addr = sock.recvfrom(4096)
    printByte(data)
    sendToAddr("com-0 accept " + str(server_address[0]), addr)
    print("waiting for ack")
    data, addr = sock.recvfrom(4096)
    global conAddr
    conAddr = addr
    print("printing addr and conAddr")
    print(addr)
    print(conAddr)
    connected = True
    printByte(data)

def recMsg():
    data, addr = sock.recvfrom(4096)
    i = 0
    if data.decode("utf-8") == "con-h 0x00":
        i = -1
    else:
        i = int(data.decode("utf-8").split(' ')[0][4:]) + 1
    printByte(data)
    return i, addr

def sendRes(i, addr):
    sendToAddr("res-" + str(i) + " I am server", addr)
    
def resetCon():
    global conAddr
    
    resetAddr = ( conAddr[0], 10001 )
    sendToAddr("con-res 0xFE", resetAddr)
    conAddr = ""
    connected = False

def connected():
    global conAddr
    sock.settimeout(4.0)
    while True:
        try:
            i, addr = recMsg()
            if addr[0] == conAddr[0] and i != -1:
                sendRes(i, conAddr)
        except socket.timeout as e:
            print("client timed out")
            resetCon()
            break
    
while True:
    waitForSyn()
    connected()
    
    
