from client import Client
import time

if __name__ == "__main__":
    client = Client(host='localhost', port=65432)
    
    # Tenta di connettersi con ritardi
    connected = False
    for attempt in range(5):
        try:
            client.connect()
            connected = True
            break
        except ConnectionRefusedError:
            if attempt < 4:
                print(f"Tentativo {attempt + 1}/5 fallito. Riprovo tra 2 secondi...")
                time.sleep(2)
            else:
                print("Impossibile connettersi al server. Assicurati che main_server.py sia in esecuzione.")
                exit(1)
    
    try:
        while True:
            msg = input("Client > ").strip()
            if not msg:
                continue
            client.send(msg)
            
            resp = client.receive()
            if resp is None:
                print("No response, disconnecting")
                break
            print(f"Server: {resp}")
            
            if msg.lower() == "quit":
                break
    finally:
        client.close()
        print("Client closed")
