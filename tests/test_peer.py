from models.peer import Peer

def test_peer():
    peer = Peer("127.0.0.1", 5000)
    peer.start_server()
    while True:
        pass

test_peer()