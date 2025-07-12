import socket
import threading

class Peer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def start_server(self):
        def handle_connection():
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((self.ip, self.port))
            server.listen()

            print(f"[Listening] on {self.ip}:{self.port}...")
            while True:
                conn, addr = server.accept()
                print(f"[Connected] with {addr}")
                threading.Thread(target=self.receive_messages, args=(conn,)).start()

        threading.Thread(target=handle_connection, daemon=True).start()

    def receive_messages(self, conn):
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    print("[Disconnected]")
                    break
                print(f"[Peer]: {data}")
            except:
                break
        conn.close()

    def connect_to_peer(self, other_peer):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((other_peer.ip, other_peer.port))
            print(f"[Connected to peer at {other_peer.ip}:{other_peer.port}]")
            while True:
                msg = input("You: ")
                client.send(msg.encode())
        except Exception as e:
            print(f"[Connection failed]: {e}")
