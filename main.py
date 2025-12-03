from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse, os, datetime, paths
# from paths import path

version = 'C2 HTTP Server 1.1'

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

# Process path
def process_path(p):

    entry = p.strip('/').split('/')

    for e in paths.paths:
        if e[0] == entry[0]:
            # [original, mapped, args]
            return [e[0], e[1], entry[1] if len(entry) > 1 else None]

    return None

# Handler
class Handler(BaseHTTPRequestHandler):

    def handle_request(self):
        length = int(self.headers.get('Content-Length', 0))
        f_path = process_path(self.path)
        r = None

        if f_path is not None:

            req = {
                'ip': self.client_address[0], 
                'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                'method': self.command, 
                'path': self.path, 
                'body': self.body.decode(errors='ignore') if length > 0 else b''
            }

            # Print Request
            out = f"Time: {req['time']}\nIP: {req['ip']}\nRequest: {req['method']} {req['path']}\n"
            
            if req['body'] != b'':
                out += f"Body: {req['body']}\n"
            
            print(out)
            if args.output != "":
                with open(args.output, 'a') as f:
                    f.write( f"\n{out}" )

            # Process Request
            if not callable(f_path[1]):
                return f_path[1]

            # Response from function => f_path[1]( arg, req )
            r = f_path[1]( f_path[2], req )
        
        # Response
        if r is None:
            r = args.response

        self.send_response(200)
        self.end_headers()
        self.wfile.write(r.encode())

    def do_GET(self): self.handle_request()
    def do_POST(self): self.handle_request()
    def do_PUT(self): self.handle_request()
    def do_DELETE(self): self.handle_request()
    def do_PATCH(self): self.handle_request()
    def do_OPTIONS(self): self.handle_request()

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    if args.version:
        print(version)
        exit(0)

    # Ensure necessary files and folders
    for nf in paths.necessary_files_folders:
        if not os.path.exists(nf):
            if nf.endswith('/'):
                os.makedirs(nf)
            else:
                open(nf, 'a').close()
    
    server = HTTPServer(("127.0.0.1" if args.local else "0.0.0.0", args.port), Handler)
    print(f"Server HTTP listening on {"127.0.0.1" if args.local else "0.0.0.0"}:{args.port}\n")
    
    # Start server
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by keyboard interrupt.", end=' ')

    server.server_close()
    print("Server closed.")