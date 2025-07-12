import time
from models.peer import Peer

def run_discovery_test():
    peer = Peer("127.0.0.1", 5003)
    peer.start_server()

    time.sleep(1)

    print("\n Discovering peers...")
    peer.discover_and_connect()

if __name__ == "__main__":
    run_discovery_test()
