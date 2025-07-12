from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('db/peer_registry.db')
cursor = conn.cursor()

class BootstrapServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/get_peers':
            pass

    def do_POST(self):
        if self.path == '/api/register':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data)
                ip = data['ip']
                port = data['port']
            except (json.JSONDecodeError, KeyError):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid JSON or missing keys')
                return

            try:
                with sqlite3.connect('db/peer_registry.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO PEERS (ip, port)
                        VALUES (?, ?)
                    ''', (ip, port))
                    conn.commit()
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'Database error: {e}'.encode())
                return

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Peer registered', 'ip': ip, 'port': port}).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def run_server():
    print("Bootstrap server running on port 8000...")
    server = HTTPServer(('0.0.0.0', 8000), BootstrapServer)
    server.serve_forever()

if __name__ == '__main__':
    run_server()