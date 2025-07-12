import time
from models.peer import Peer

def run_driver():
    peer1 = Peer("127.0.0.1", 5000)
    peer2 = Peer("127.0.0.1", 5001)

    peer1.start_server()
    peer2.start_server()

    time.sleep(1)

    print("\n🧪 Peer-to-Peer Chat Test")
    print("1. Peer1 connects to Peer2")
    print("2. Peer2 connects to Peer1")
    choice = input("Choose connection direction (1 or 2): ")

    if choice == "1":
        peer1.connect_to_peer(peer2)
    elif choice == "2":
        peer2.connect_to_peer(peer1)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    run_driver()
