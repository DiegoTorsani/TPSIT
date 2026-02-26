import socket

class Server:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(1)
        print(f"Server listening on {self.host}:{self.port}")
        conn, addr = s.accept()
        print("Connected by", addr)
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode().strip()
                print(f"Client: {msg}")
                
                if msg.lower() == "quit":
                    conn.sendall(b"Goodbye")
                    break
                
                # Server risponde al messaggio ricevuto
                response = input("Server > ").strip()
                if response:
                    conn.sendall(response.encode())
                if response.lower() == "quit":
                    break
        s.close()
        print("Server stopped")