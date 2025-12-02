from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse, os
from util import request_proccessor as req_proc

version = 'C2 HTTP Server 1.0'

# Args
parser = argparse.ArgumentParser(description="Command and Control HTTP Server")

# Version
parser.add_argument('-v', '--version', action='store_true', help='Show version')

# Port
parser.add_argument('-p', '--port', type=int, default=4443, help='Listening port')

# Response options
parser.add_argument('--response', type=str, default='OK', help='Response message')

# Other options
parser.add_argument('--local', action='store_true', help='Local IP only (not implemented)')
parser.add_argument('-O', '--output', default="", type=str, help='Output file (not implemented)')

args = parser.parse_args()

# Handler
class Handler(BaseHTTPRequestHandler):

    def basic_request(self):
        length = int(self.headers.get('Content-Length', 0))

        r = req_proc( 
            self,
            self.client_address[0], 
            self.command, 
            self.path, 
            self.rfile.read(length) if length > 0 else b'' ,
            output_file=args.output
        )

        # Response
        if r is None:
            r = args.response

        self.send_response(200)
        self.end_headers()
        self.wfile.write(r.encode())

    def do_GET(self):
        self.basic_request()
    
    def do_POST(self):
        self.basic_request()

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    if args.version:
        print(version)
        exit(0)
    
    server = HTTPServer(("127.0.0.1" if args.local else "0.0.0.0", args.port), Handler)
    print(f"Server HTTP listening on {"127.0.0.1" if args.local else "0.0.0.0"}:{args.port}\n")
    server.serve_forever()