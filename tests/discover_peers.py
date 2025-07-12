import time
from models.peer import Peer  # Adjust the import path if needed

def run_discovery_test():
    # Define this peer
    peer = Peer("127.0.0.1", 5003)  # You can change the port for each peer
    peer.start_server()

    # Let the server start and stabilize
    time.sleep(1)

    # Discover and ping all other peers
    print("\n🔍 Discovering peers...")
    peer.discover_and_connect()

if __name__ == "__main__":
    run_discovery_test()
