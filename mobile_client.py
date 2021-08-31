from socket import *



def update_client_list(serName,serPort):            #Creates connections to update the list of appliances
    size = find_client_size(serName,serPort)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serName,serPort))
    line = str.encode("app3")
    clientSocket.send(line)
    client_str_bytes = clientSocket.recv(2**size)
    client_str = client_str_bytes.decode()
    return client_str.split(",")
    


def find_client_size(serName,serPort):              #finds the bit size of the amount of appliances so recv() doesnt overflow
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serName,serPort))
    line = str.encode("app2")
    clientSocket.send(line)
    size_bytes = clientSocket.recv(16)
    size = int(size_bytes.decode())  
    clientSocket.close()
    return size

clients = []
machineState = 0
serverName =  "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clients = update_client_list(serverName,serverPort)
while 1:
    print("Mobile")
    print("")
    
    for i in clients:                   #input interactions between user and .py
        print(i)
    
    clientchosen = int(input("Enter which appliance list above which do you want to change(choose 0 or 1 or 2...):"))
    while(clientchosen > len(clients)):
        clientchosen = input("appliance chosen doesnt exist in the list, choose again(choose 0 or 1 or 2...):" )
    client_Name = clients[clientchosen] 
    
    number_code = input("Do you want to turn the machine on/off(0/1):")
    while(number_code !="0" and number_code != "1"):                        #error handling
        number_code = input("Invalid state, try again (0/1):")
    Exit = input("do you want to exit (y/n):")
    if (Exit == 'y'):  
        break                                   
    clients = update_client_list(serverName,serverPort)
    if(clientchosen > len(clients)):
        print("Error- Requested appliance is not available. Please try again")
    elif(clients[clientchosen] != client_Name):
        print("Error- Requested appliance is not available. Please try again")
    else:
        clientSocket = socket(AF_INET, SOCK_STREAM)    
        clientSocket.connect((serverName,serverPort))           #tcp connection
        sentence = str.encode("app"+number_code+clients[clientchosen])
        clientSocket.send(sentence)
        modifiedSentence = clientSocket.recv(1024)
        print ("From Server:", modifiedSentence.decode())
        print(" ")
        clientSocket.close()

