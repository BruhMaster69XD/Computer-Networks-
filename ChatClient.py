import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_port = ("143.47.184.219", 5378)
sock.connect(host_port)


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
      
        
        
            
        
    while True:


            MainInput= input(" Please enter a command: ")
                
            if MainInput == "!WHO":
                whoToClient = "WHO"
                whoToClient += "\n"
                WhoString_bytes = whoToClient.encode("utf-8")
                sock.sendall(WhoString_bytes)
                WhoData = sock.recv(4096)
                WhoDecoded = WhoData.decode()
                print(WhoDecoded) 
                
            elif MainInput == "!QUIT":
                print("You are now being logged off")
                OurProgram()
            elif MainInput == "Read messages":

                rData = sock.recv(4096)

                rDecoded = rData.decode()
                print(rDecoded)
                
            


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

                MessageData = sock.recv(4096)

                MessageDecoded = MessageData.decode()
                
                MessageDecoded = MessageDecoded [:-1]
                if MessageDecoded ==  "SEND-OK":
                    print("Message sent sucesfully")
                elif MessageDecoded == "UNKNOWN":
                    print ("The user your sending this message to is not logged in")
                else:
                    print (MessageDecoded)


OurProgram()
