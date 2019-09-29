import time
import threading
import socket
import configparser

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
autoSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_address = ('localhost', 10001)
autoSocket.bind(client_address)
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
server_address = ('localhost', 10000)
conCount = 0

connected = False
conAddr = None

parser = configparser.RawConfigParser()
parser.read("./opt.conf")
keepalive = parser.getboolean('client', 'keepalive')

def printByte(data):
    print(data.decode("utf-8"))

def sendToAddr(msg, addr):
    msg = msg.encode("utf-8")
    sent = sock.sendto(msg, addr)

def sendToCon(msg):
    sendToAddr(msg, conAddr)

def verifySynAck(msg, addr):
    print(msg)
    if msg == "com-0 accept " + str(server_address[0]):
        print("verified")
        return True
    print("Not verified")
    return False

def syn():
    print("start syn")
    sendToAddr("com-0 " + str(ip), server_address)
    data, addr = sock.recvfrom(4096)
    success = verifySynAck(data.decode("utf-8"), addr)
    printByte(data)
    sendToAddr("com-0 accept", server_address)
    global conAddr
    global connected
    conAddr = addr
    connected = True
    return success

def sendInputMsg(i):
    msg = "msg-" + str(i) + " " + input()
    if connected != False:
        sendToAddr(msg, server_address)

def sendAutoMsg(i, msg):
    msg = "msg-" + str(i) + " " + msg
    if connected != False:
        sendToAddr(msg, server_address)

def recMsg():
    global conCount
    data, addr = sock.recvfrom(4096)
    conCount = int(data.decode("utf-8").split(' ')[0][4:]) + 1
    printByte(data)
    return conCount, addr

def listenForReset():
    global connected
    while True:
        data, addr = autoSocket.recvfrom(4096)
        if data.decode("utf-8") == "con-res 0xFE":
            printByte(data)
            sendToCon("con-res 0xFF")
            connected = False
            conAddr = None
            break
        
def heartbeat():
    while True:
        time.sleep(3.0)
        sendToCon("con-h 0x00")
        
def sendAuto():
    threading.Thread(target=listenForReset).start()
    while True:
        if connected == True:
            sendAutoMsg(conCount, "spam")
            i, addr = recMsg()
        else:
            break
        
def chat():
    threading.Thread(target=listenForReset).start()
    if keepalive == True:
        threading.Thread(target=heartbeat).start()
        while True:
            sendInputMsg(conCount)
            if connected == False:
                break
            i, addr = recMsg()
        
def main():
    global conCount
    while True:
        success = syn()
        if success:
            if auto:
                sendAuto()
            else:
                chat()
                
main()

