import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
server_address = ('localhost', 10000)
i = 0

def printByte(data):
    print(data.decode("utf-8"))

def sendToAddr(msg, addr):
    msg = msg.encode("utf-8")
    sent = sock.sendto(msg, addr)

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
    return success

def sendMsg(i):
    msg = "msg-" + str(i) + " " + input()
    sendToAddr(msg, server_address)

def recMsg():
    data, addr = sock.recvfrom(4096)
    i = int(data.decode("utf-8").split(' ')[0][4:]) + 1
    printByte(data)
    return i, addr

while True:
    success = syn()
    if success:
        while True:
            sendMsg(i)
            i, addr = recMsg()
    
