#!/usr/bin/env python3


import http.server
import socketserver
import threading

class HTTPServerThread (threading.Thread):
    def __init__(self, PORT):
        threading.Thread.__init__(self)
        self.PORT = PORT
    def run(self):
        Handler = http.server.SimpleHTTPRequestHandler
        socketserver.TCPServer.allow_reuse_address = True
        httpd = socketserver.TCPServer(("", self.PORT), Handler)
        httpd.serve_forever()