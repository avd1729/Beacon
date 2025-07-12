from http.server import HTTPServer
from models.bootstrap_server import BootstrapServer

def run_server():
    print("Bootstrap server running on port 8000...")
    server = HTTPServer(('0.0.0.0', 8000), BootstrapServer)
    server.serve_forever()

if __name__ == '__main__':
    run_server()