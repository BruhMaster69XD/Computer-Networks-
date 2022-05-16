from lzma import FORMAT_RAW
import threading
import socket
import array
from collections import defaultdict

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)


clients = set()
clients_lock = threading.Lock()
 
username_dict = defaultdict() 



def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")    
    try:
    
        while True:
            user = conn.recv(1024).decode(FORMAT)
            

            user= user[11:]
            user = user[:-1]
        
        
            if user in username_dict:
                inUse = ("IN-USE\n").encode("utf-8")
                conn.sendall(inUse)
            else :   
                if len(username_dict) > 64:
                    TooManyUsers= "BUSY"
                    TooManyUsers= "\n"
                    TooManyUsers= TooManyUsers.encode()
                    conn.sendall(TooManyUsers)
            
                username_dict[user] = conn
                serverHandshake = ("HELLO ")
                serverHandshake += user 
                serverHandshake += ("\n")
                serverHandshake = serverHandshake.encode("utf-8")
                conn.sendall(serverHandshake)
        
        
                while True:

                    commands = conn.recv(1024).decode(FORMAT)
                    ifMessage = commands
                    ifMessage= ifMessage.split()[0]


                
                    if commands == "WHO\n":
                        listOfNames = "WHO-OK "
                        listOfNames += ",".join(username_dict.keys())
                        listOfNames += " \n"
                        listOfNames = listOfNames.encode("utf-8")
                        conn.sendall(listOfNames)
                    elif ifMessage == "SEND":
                        commandsUsername = commands.split(" ")[1]
                        commandsMessage = commands.split(' ',1)[1]
                        commandsMessage = commandsMessage.split(' ',1)[1]
                        if commandsUsername in username_dict.keys():
                            newConn = username_dict.get(commandsUsername)
                            MessageToSend = "DELIVERY "
                            MessageToSend += user
                            MessageToSend += " "
                            MessageToSend += commandsMessage
                            MessageToSend += "\n"
                            MessageToSend = MessageToSend.encode("utf-8")
                            newConn.sendall(MessageToSend)
                            MessagetoSender = "SEND-OK"
                            MessagetoSender += "\n"
                            MessagetoSender =MessagetoSender.encode("utf-8")
                            conn.sendall(MessagetoSender)
                        else:
                            UserUnknown = "UNKNOWN"
                            UserUnknown += "\n"
                            UserUnknown = UserUnknown.encode("utf-8")
                            conn.sendall(UserUnknown)
                    else:
                        badHeader = "BAD-RQST-HDR"
                        badHeader += "\n"
                        badHeader = badHeader.encode("utf-8")
                        conn.sendall(badHeader)
                        

                
        
            # string = ("HELLO Philipp\n").encode("utf-8")
            # conn.sendall(string)
            # string = ("Delivery Philipp yo whats up\n").encode("utf-8")
            # conn.sendall(string)
                



     
    finally:
        with clients_lock:
            clients.remove(conn)

        conn.close()


def start():
    print('[SERVER STARTED]!')
    server.listen()
    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon = True)
        thread.start()
       

    
start()
