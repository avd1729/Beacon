import unittest
from models.peer import Peer

class TestPeer(unittest.TestCase):
    def test_peer_creation(self):
        peer = Peer("127.0.0.1", 5000)
        self.assertEqual(peer.ip, "127.0.0.1")
        self.assertEqual(peer.port, 5000)

if __name__ == '__main__':
    unittest.main()
