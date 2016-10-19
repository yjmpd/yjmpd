#!/usr/bin/env python3
import http.server
import os
import urllib

import socketserv as socketserv
import threading
import html
import ssl


"""
HTTP request handler.
"""


class HTTPServerThread(threading.Thread):
    def __init__(self, port, api, musicdir, certfile):
        threading.Thread.__init__(self)
        self.PORT = port
        self.API = api
        self.musicdir = musicdir
        self.certfile = certfile

    def run(self):
        Handler = HTTPHandler
        socketserv.TCPServer.allow_reuse_address = True
        httpd = socketserv.ThreadingTCPServer(("", self.PORT), Handler, self.API)
        httpd.socket = ssl.wrap_socket(httpd.socket, certfile=self.certfile, server_side=False)
        os.chdir(self.musicdir)
        httpd.serve_forever()


"""
HTTP calls
"""


class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.api = server.api
        http.server.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    def send_message(self, status, content_type, data):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(data)
        self.wfile.write("\n".encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Methods", "GET,HEAD,PUT,DELETE,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write("\n".encode("utf-8"))

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        """ Serve a GET request. """
        args = str(urllib.parse.unquote(self.path))
        args = args.split('?')
        path = (html.unescape(args[0]))
        if len(args) >= 2:
            del args[0]
            args = args[0].split('&')

        result = self.api.apigetcall(path, args)
        if result:
            self.send_message(200, "application/json", result)
        else:
            f = self.send_head()
            print(f)
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()

    def do_DELETE(self):
        """ Serve a GET request. """
        path = html.unescape(self.path)
        self.send_message(200, "application/json", self.api.apideletecall(path, ""))

    def do_PUT(self):
        """ Serve a PUT request. """
        if self.headers["Content-Type"] == 'application/json':
            length = int(self.headers["Content-Length"])
            rawdata = self.rfile.read(length)
            path = html.unescape(self.path)
            self.send_message(200, "application/json", self.api.apiputcall(path, rawdata))
        else:  # Content type not correct
            self.send_message(403, "application/json", self.api.jsonify({"error": "Content type not accepted"}))

    def do_POST(self):
        """ Serve a POST request. """
        if self.headers["Content-Type"] == 'application/json':
            length = int(self.headers["Content-Length"])
            rawdata = self.rfile.read(length)
            path = html.unescape(self.path)
            self.send_message(200, "application/json", self.api.apipostcall(path, rawdata))
        else:  # Content type not correct
            self.send_message(403, "application/json", self.api.jsonify({"error": "Content type not accepted"}))

