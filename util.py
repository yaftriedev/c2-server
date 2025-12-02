from datetime import datetime
from paths import path

# Request function
def request_proccessor(handler, ip, method, path, body, output_file=""):
    
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f_path = process_path(path)
    
    if f_path is not None:

        print_request(ip, time, method, path, body, output_file=output_file)
        
        # Process Request
        # original => f_path[0]
        # matched => f_path[1]
        # args => f_path[2]
        if not callable(f_path[1]):
            return f_path[1]

        return f_path[1]( f_path[2], {'ip': ip, 'time': time, 'method': method, 'path': path, 'body': body} )
    
    return None

# Print request
def print_request(ip, time, method, path, body, output_file=""):
    
    out = f"Time: {time}\nIP: {ip}\nRequest: {method} {path}\n"
    
    if body != b'':
        out += f"Body: {body.decode(errors='ignore')}\n"
    
    print(out)
    if output_file != "":
        with open(output_file, 'a') as f:
            f.write( f"\n{out}" )

# Comprove path
def process_path(p):

    entry = p.strip('/').split('/')

    for e in path:
        if e[0] == entry[0]:
            # [original, mapped, args]
            return [e[0], e[1], entry[1] if len(entry) > 1 else None]

    return None
