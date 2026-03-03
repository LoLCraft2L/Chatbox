#Imports
import socket

#Main Set-up
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.host = "127.0.0.1"
        self.port = 65432
        self.addr = (self.host, self.port)
        
        
        self.client.connect(self.addr)
        

        message = "A new user has joined the chat!"
        self.client.send(message.encode("utf-8"))
        
    def send_message(self, message):
        self.client.send(message.encode("utf-8"))

