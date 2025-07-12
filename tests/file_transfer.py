import time
from models.peer import Peer

def run_driver():
    peer1 = Peer("127.0.0.1", 5000)
    peer2 = Peer("127.0.0.1", 5001)

    peer1.start_server()
    peer2.start_server()

    time.sleep(1)

    # Hardcoded file path
    filepath = "docs/sample.txt"

    print("\n Peer-to-Peer File Sharing Test")
    print("1. Peer1 sends file to Peer2")
    print("2. Peer2 sends file to Peer1")
    choice = input("Choose direction (1 or 2): ")

    if choice == "1":
        peer1.connect_to_peer(peer2, filepath)
    elif choice == "2":
        peer2.connect_to_peer(peer1, filepath)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    run_driver()
