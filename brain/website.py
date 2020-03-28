import http.server
import re


class Website:
    def __init__(self):
        self.paths = {}

    def route(self, path):
        def decorator(f):
            self.paths[path] = f
            return f

        return decorator

    def run(self, address):
        paths = self.paths

        class Handler(http.server.BaseHTTPRequestHandler):
            def send_body(self, res, body):
                body = body.encode()
                self.send_response(res)
                if res == 200:
                    self.send_header('Content-Type', 'text/html')
                    self.send_header('Content-Length', len(body))
                    self.end_headers()
                    self.wfile.write(body)
                else:
                    self.end_headers()

            def do_GET(self):
                if self.path in paths:
                    func = paths[self.path]
                    res, body = func()
                    self.send_body(res, body)
                    return
                for path in paths:
                    match = re.search(path, self.path)
                    if match and match.groups():
                        func = paths[path]
                        res, body = func(*match.groups())
                        if res != 200:
                            self.send_response(res)
                            self.end_headers()
                            return
                        self.send_body(res, body)
                        return
                self.send_response(404)
                self.end_headers()

        http_server = http.server.HTTPServer(address, Handler)
        try:
            http_server.serve_forever()
        except KeyboardInterrupt:
            http_server.socket.close()
