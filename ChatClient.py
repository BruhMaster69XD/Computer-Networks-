import socket
import threading




def readMessages(sock):
    while True:
        rData = ""
        while True:
            rData = sock.recv(4096)
            # accumulator2 = accumulator2.decode()
            # checker2 = accumulator2[-1]
            # rData +=  accumulator2
            # if checker2 == "\n":
            #     break
            rData = rData.decode()
            if rData == "":
                break
            else :
                rData2 = rData.split()[0]
                if rData2 == "WHO-OK":
                    print(rData)
                elif rData2 == "SEND-OK":
                    print("your message was sent succesfully")
                elif rData2 == "BUSY":
                    print("sorry fam you aint getting in")
                elif rData2 == "UNKNOWN":
                    print("user is not logged in")
                elif rData2 == "BAD-RQST-HDR":
                    print("your header was incorrect")
                elif rData2 == "BAD-RQST-BODY":
                    print("something went wrong with your body")
                else:
                    rData = rData[8:]
                    print(rData)




def OurProgram(sock) :


    message = "HELLO-FROM "
    message += input("please enter a username: ")
    message += "\n"
    string_bytes = message.encode("utf-8")
    sock.sendall(string_bytes)

    data = ""

    while True:
            accumulator2 = sock.recv(1)
            accumulator2 = accumulator2.decode()
            checker2 = accumulator2[-1]
            data +=  accumulator2
            if checker2 == "\n":
                break

    decoded = data
    decoded = decoded [:-1]

            
    while decoded == "IN-USE":
        
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_port = ("143.47.184.219", 5378)
        sock.connect(host_port)

        print("the username was already taken")
        message = "HELLO-FROM "
        message += input("please enter a username: ")
        message += "\n"
        string_bytes = message.encode("utf-8")
        sock.sendall(string_bytes)

        data = sock.recv(4096)

        decoded = data.decode()
        decoded = decoded [:-1]
        print(decoded)

        

    t = threading.Thread(target=readMessages, args = (sock,))
    t.daemon = True
      
        
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
                break
                
                

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
           


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_port = ("localhost", 5050)
sock.connect(host_port)

OurProgram(sock)