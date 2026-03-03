#IMPORTS
import socket
from _thread import start_new_thread

#Initialize connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

no_of_clients = 0
all_clients = []

HOST = "127.0.0.1"
PORT = 65432

#Host a server 
try: 

    server.bind((HOST,PORT))

except socket.error as error_message:

    print(str(error_message))


server.listen()
print("Looking for Connection...")


def broadcast_message (current_sender, message):
    """
        Send the received text to all users except the user who sent it..
        if it detects dead client it will attempt to remove the dead client
    """
    global all_clients
    global no_of_clients
    for client in all_clients[:]: 
        if client != current_sender:
            try:
                client.send(message)
            except: 
                if client in all_clients:
                    all_clients.remove(client)
                    print("Connection Lost...")
                    no_of_clients-=1
                    print("Total no of client", no_of_clients)

#Handle the server
def threaded_client(client):
    global no_of_clients
    global all_clients
    while True:
        try:
            data = client.recv(2048)
            if not data:
                client.close()
                break
            else:
                broadcast_message(client,data)  
        except:
            break

    if client in all_clients:
        all_clients.remove(client)
        no_of_clients -= 1
        disconnection = "A user has been disconnected!"
        broadcast_message(client,disconnection.encode("utf-8"))
        print(f"Connection closed. Total: {no_of_clients}")
        print("Total no of client", no_of_clients)
    
    client.close()

while True:
    (client, address) = server.accept()
    no_of_clients +=1
    print("Successfully connected to a client!")
    all_clients.append(client)
    start_new_thread(threaded_client, (client,))