import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

# Store the latest weight data
latest_weight = {"weight": 0, "timestamp": datetime.now().isoformat()}

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            global latest_weight
            latest_weight = {
                "weight": data.get("weight", 0),
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"Received weight: {latest_weight['weight']} KG at {latest_weight['timestamp']}")
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())
            
        except Exception as e:
            print(f"Error processing request: {e}")
            self.send_response(500)
            self.end_headers()
    
    def do_GET(self):
        try:
            if self.path == '/weight':
                response_data = {
                    "weight": latest_weight["weight"],
                    "timestamp": latest_weight["timestamp"]
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode())
            else:
                self.send_response(404)
                self.end_headers()
            
        except Exception as e:
            print(f"Error processing GET request: {e}")
            self.send_response(500)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server():
    # Use PORT environment variable for hosting platforms
    port = int(os.environ.get('PORT', 8000))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, RequestHandler)
    
    print(f'🚀 Drip Monitor Server running on port {port}...')
    print('📊 Weight endpoint: /weight')
    print('Press Ctrl+C to stop the server')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")

if __name__ == '__main__':
    run_server()