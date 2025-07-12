from http.server import HTTPServer
from models.bootstrap_server import BootstrapServer
from models.peer import Peer

def run_server():
    print("Bootstrap server running on port 8000...")
    server = HTTPServer(('0.0.0.0', 8000), BootstrapServer)
    server.serve_forever()


run_server()