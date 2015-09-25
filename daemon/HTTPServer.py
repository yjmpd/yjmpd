import http.server
import socketserver
import threading

import daemon.API as API


class HTTPServerThread(threading.Thread):
    def __init__(self, PORT):
        threading.Thread.__init__(self)
        self.PORT = PORT

    def run(self):
        Handler = HTTPHandler
        socketserver.TCPServer.allow_reuse_address = True
        httpd = socketserver.TCPServer(("", self.PORT), Handler)
        httpd.serve_forever()


testdata = []


class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Serve a GET request."""
        retval = API.calls.APIcall(str(self.path).lstrip("/"), "get")
        if retval is not None:
            self.send_response(200)
            self.send_header("Content-type:", "application/json")
            self.end_headers()
            self.wfile.write(retval)
            self.wfile.write("\n".encode("utf-8"))
        else:
            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()

    def do_POST(self):
        retval = API.calls.APIcall(str(self.path).lstrip("/"), "post")
        if retval is not None:
            if self.headers["Content-Type"] == 'application/json':
                length = int(self.headers["Content-Length"])
                rawdata = self.rfile.read(length)
                result = retval(API.calls.getfromjson(rawdata,"data"))
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(result)
                self.wfile.write("\n".encode("utf-8"))
            else:
                self.send_response(422)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(API.calls.jsonify({"error":"Not JSON data."}))
                self.wfile.write("\n".encode("utf-8"))
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
