from socket import *
import math
import time
#Code made by Cornell Castelino, Shouray Duggal, David Ryan and Radhika Verma
#server

def update_server_list(servers):                #removes psuedo-servers that have
    print("inside")
    for i in reversed(range(len(servers))):     #disconnected from the server
        socket = servers[i][1]
        try:
            socket.send(str.encode("2"))
            x = socket.recv(1024)               #variable is unsed since its just to check 
        except:                                 #if recv() is a succes or it returns an exception
            print(servers[i][0]+" disconnected")#if recv pops an exception 
            servers.pop(i)
    return servers
        
serverPort = 12000                              #server initialisation
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('localhost',serverPort))
serverSocket.listen(1)
#----------------------------------------------
print ("The server is ready to receive")
#----------------------------------------------
servers= []     #appliance list
TimeOut= {}     #
code_word = "app"
check2 = False                              #bool for existance of the appliance in the list

while 1:
    connectionSocket, addr = serverSocket.accept()
    connectionSocket1 = connectionSocket
    sentence_bytes = connectionSocket.recv(1024)
    sentence = sentence_bytes.decode()  
    print(sentence)
    sentence = sentence.lower()   
    print(sentence)
    check = True                            #bool for existance of the appliance in the list
    
    if(sentence == "close"):              #force shutdown of the server
        break

    if(sentence[0:3] == code_word):
        print("connection with "+code_word+sentence[3])         #for mobile_client
        data = sentence[3]
        ser_Name = sentence[4:]
        
        string = ""                              #creates a string of all servers to send  
        servers = update_server_list(servers)    #to the mobile client for upto date client info
        print("after")
        for i in range(len(servers)):
            string += servers[i][0] + ","
        string = string[:-1]
        
        if( data == "2"):                            #sends the client the size of the client list
            print("client-Size Sent")
            size = math.floor(math.log(len(string),2)) + 1
            connectionSocket.send(str.encode(str(size)))
            
            connectionSocket.close()

        if( data == "3"):                            # returns a list of servers
            print("Appliance list Sent")
            connectionSocket.send(str.encode(string))
            connectionSocket.close()

        if(data == "1" or data == "0"):             #informs the other servers to change its state
            for i in range(len(servers)):           #checks if client exists in the list  
                if(servers[i][0]==ser_Name):
                    connectionSocket = servers[i][1]
                    check = False
         
            if(check):                              #if it doesnt exist return an error
                connectionSocket.send(str.encode("Error: device does not exist in network"))
                connectionSocket.close()
            else:
                connectionSocket.send(str.encode(data))
            
                success = connectionSocket.recv(1024)    #small communication to know that    
                connectionSocket1.send(success)          #the other servers received the msg
                connectionSocket1.close()
    else:                                           #append new client connections to 
        print("connection with "+  sentence)        #the list for mobile client to know
        if(check2): 
            for i in reversed(range(len(servers))): #removes old connection
                if(servers[i][0] == sentence):
                    servers.pop(i)
        servers.append([sentence,connectionSocket]) #appends new connections
        check2 = True
    print(" ")

  

