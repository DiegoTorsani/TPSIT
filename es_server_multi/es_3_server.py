import socket
import threading

class ServerThread(threading.Thread):
    def __init__(self, client_socket):
        super().__init__()
        self.client = client_socket

    def run(self):
        try:
            self.comunica()
        except Exception as e:
            print(f"Errore nel thread: {e}")

    def comunica(self):
        with self.client:
            input_client  = self.client.makefile('r', encoding='utf-8')
            output_client = self.client.makefile('w', encoding='utf-8')

            while True:
                stringa_ricevuta = input_client.readline().rstrip('\n')

                if stringa_ricevuta is None or stringa_ricevuta == "FINE":
                    output_client.write(stringa_ricevuta + " (=>server in chiusura...)\n")
                    output_client.flush()
                    print(f"server in chiusura :{stringa_ricevuta}")
                    break
                else:
                    output_client.write(stringa_ricevuta + " (ricevuta e ritrasmessa)\n")
                    output_client.flush()
                    print(f"server :{stringa_ricevuta}")

            print(f"9 Chiusura socket {self.client.getpeername()}")


class MultiServer:
    def start(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('', 6789))
            server_socket.listen()

            while True:
                print("1 Server in attesa ...")
                client_socket, addr = server_socket.accept()
                print(f"3 Server socket {client_socket}")

                server_thread = ServerThread(client_socket)
                server_thread.start()

        except Exception as e:
            print(e)
            print("Errore durante l'istanza del server!")


if __name__ == "__main__":
    tcp_server = MultiServer()
    tcp_server.start()