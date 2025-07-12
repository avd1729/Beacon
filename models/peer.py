import socket
import threading
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
bootstrap_server_url = os.getenv("BOOTSTRAP_SERVER_URL")

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
        try:
            # Read header first (assumes header ends with newline)
            header_data = b''
            while not header_data.endswith(b'\n'):
                header_data += conn.recv(1)
            header = json.loads(header_data.decode())

            if header["type"] == "file":
                filename = header["filename"]
                filesize = header["filesize"]

                print(f"[Receiving] {filename} ({filesize} bytes)...")
                with open(f"received_{filename}", "wb") as f:
                    received = 0
                    while received < filesize:
                        chunk = conn.recv(min(1024, filesize - received))
                        if not chunk:
                            break
                        f.write(chunk)
                        received += len(chunk)
                print(f"[Received File] saved as received_{filename}")
            else:
                print(f"[Unknown header type]: {header}")

        except Exception as e:
            print(f"[Error receiving]: {e}")
        finally:
            conn.close()


    def connect_to_peer(self, other_peer, filepath=None):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((other_peer.ip, other_peer.port))
            print(f"[Connected to peer at {other_peer.ip}:{other_peer.port}]")

            if filepath and os.path.exists(filepath):
                filename = os.path.basename(filepath)
                filesize = os.path.getsize(filepath)

                header = json.dumps({
                    "type": "file",
                    "filename": filename,
                    "filesize": filesize
                }).encode()
                client.send(header + b'\n')

                # Send file in chunks
                with open(filepath, 'rb') as f:
                    while chunk := f.read(1024):
                        client.send(chunk)

                print(f"[File Sent] {filename} ({filesize} bytes)")
            else:
                print("No valid file specified")

        except Exception as e:
            print(f"[Connection failed]: {e}")
        finally:
            client.close()


    def register_as_peer(self):
        peer_data = {
            "ip" : self.ip,
            "port" : self.port
        }
        try:
            response = requests.post(bootstrap_server_url + "/api/register", json=peer_data)
            print("Status Code:", response.status_code)
            print("Response JSON:", response.json())
        except requests.exceptions.RequestException as e:
            print("Error communicating with bootstrap server:", e)

    def get_all_peers(self):
        try:
            response = requests.get(bootstrap_server_url + "/api/get_peers")
            print("Status Code:", response.status_code)
            
            if response.status_code == 200:
                data = response.json()
                print("Received Peers List:")
                for peer in data.get("peers", []):
                    print(f"IP: {peer['ip']}, Port: {peer['port']}")
            else:
                print("Failed to retrieve peers.")

        except requests.exceptions.RequestException as e:
            print("Error:", e)

