import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_port = ("143.47.184.219", 5378)
sock.connect(host_port)

def readMessages():
    while True:
        
        rData = sock.recv(4096)
        rData2 = rData
        rData2 = rData2[0:7]
        rData = rData.decode("utf-8")
        rData2 = rData2.decode("utf-8")
        if rData2 == "WHO-OK":
            print(rData)
        elif rData2 == "SEND-Ok":
            print("your message was sent succesfully")
        elif rData2 == "UNKNOWN":
            print("user is not logged in")
        else:
            rData = rData[8:]
            print(rData)

t = threading.Thread(target=readMessages)

def OurProgram() :


    message = "HELLO-FROM "
    message += input("please enter a username: ")
    message += "\n"
    string_bytes = message.encode("utf-8")
    sock.sendall(string_bytes)

    data = sock.recv(4096)

    decoded = data.decode()
    decoded = decoded [:-1]

            
    while decoded == "IN-USE":
        print("the username was already taken")
        message = "HELLO-FROM "
        message += input("please enter a username: ")
        message += "\n"
        string_bytes = message.encode("utf-8")
        sock.sendall(string_bytes)

        data = sock.recv(4096)

        decoded = data.decode()
        decoded = decoded [:-1]
      
        
    t.start()

        
    while True:
      
            MainInput= input(" Please enter a command (or wait for message): ")
           

                
            if MainInput == "!WHO":
                whoToClient = "WHO"
                whoToClient += "\n"
                WhoString_bytes = whoToClient.encode("utf-8")
                sock.sendall(WhoString_bytes)
                
                
            elif MainInput == "!QUIT":
                print("You are now being logged off")
                OurProgram()
                

            else:
                MainInput = MainInput[1:]
                MessageInput= input("Whats your message ?: ")
                MessageToUser = "SEND "
                MessageToUser += MainInput
                MessageToUser += " "
                MessageToUser += MessageInput
                MessageToUser += "\n"

                MessageToUser_bytes = MessageToUser.encode("utf-8")
                sock.sendall(MessageToUser_bytes)
           


OurProgram()
