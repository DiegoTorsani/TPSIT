import socket

class Client:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")

    def send(self, message):
        self.sock.sendall(message.encode())

    def receive(self):
        data = self.sock.recv(1024)
        if not data:
            return None
        return data.decode()

    def close(self):
        self.sock.close()