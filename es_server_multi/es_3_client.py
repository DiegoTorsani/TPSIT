import socket

def main():
    host = '127.0.0.1'
    port = 6789

    try:
        with socket.create_connection((host, port)) as s:
            r = s.makefile('r', encoding='utf-8')
            w = s.makefile('w', encoding='utf-8')

            print(f"Connesso a {host}:{port}. Digita 'FINE' per terminare.")
            while True:
                msg = input("> ").strip()
                if not msg:
                    continue

                w.write(msg + "\n")
                w.flush()

                risposta = r.readline()
                if risposta == "":
                    print("Connessione chiusa dal server.")
                    break

                print(f"Server: {risposta.rstrip()}")

                if msg == "FINE":
                    # dopo aver inviato FINE il server risponde e chiude
                    break

    except ConnectionRefusedError:
        print("Impossibile connettersi: server non in ascolto su", host, port)
    except KeyboardInterrupt:
        print("\nTerminato dall'utente.")
    except Exception as e:
        print("Errore:", e)

if __name__ == "__main__":
    main()