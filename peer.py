import socket
import threading

def start_server(my_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', my_port))
    server.listen(1)
    print(f"Listening on port {my_port}...")

    conn, addr = server.accept()
    print(f"Connection from {addr}")

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                print("Peer disconnected.")
                break
            print(f"[Peer]: {data}")
        except:
            break

def start_client(target_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('127.0.0.1', target_port))
        print(f"Connected to peer on port {target_port}")
        while True:
            msg = input("You: ")
            client.send(msg.encode())
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    role = input("Do you want to be a server or client? (s/c): ").strip().lower()

    my_port = int(input("Enter your port to listen on: ").strip())

    if role == 's':
        start_server(my_port)
    elif role == 'c':
        target_port = int(input("Enter peer's port to connect to: ").strip())
        # Start listening in the background in case peer also sends messages back
        threading.Thread(target=start_server, args=(my_port,), daemon=True).start()
        start_client(target_port)
    else:
        print("Invalid role. Please enter 's' or 'c'.")
