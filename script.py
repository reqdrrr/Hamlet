import http.server
import socketserver
from query import chat


PORT = 8080
DIRECTORY = 'public'

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_POST(self):
        self.send_response(200)
        content_length = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_length)
        self.end_headers()
        reply = chat(post_body.decode())
        self.wfile.write(str.encode(reply))

with socketserver.TCPServer(('', PORT), Handler) as httpd:
    print('serving at port', PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()