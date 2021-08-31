from socket import *
import time
serverName =  "192.168.0.235"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
serName = "lights"
while 1:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    sentence = str.encode(serName)                 #The message indicating the appliance name
    print(serName)
    clientSocket.send(sentence)
    
    modifiedSentence = clientSocket.recv(1024)      #receives a number code(0,1,2) with 0,1 indicating switch on/off
    while(modifiedSentence == b'2'):                #receving number 2 indicates a keepalive message for the server to figure out if this appliance is active
        clientSocket.send(str.encode("1"))
        modifiedSentence = clientSocket.recv(1024)
    print ("From Server:", modifiedSentence.decode())
    clientSocket.send(str.encode("1"))
clientSocket.close()