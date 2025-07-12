from models.peer import Peer

if __name__ == "__main__":
    peer = Peer("127.0.0.1", 5000)
    peer.register_as_peer()