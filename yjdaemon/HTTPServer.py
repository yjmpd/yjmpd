#!/usr/bin/env python3


import http.server
import socketserver
import threading

import yjdaemon.API as API

"""
HTTP request handler.
"""


class HTTPServerThread(threading.Thread):
    def __init__(self, PORT):
        threading.Thread.__init__(self)
        self.PORT = PORT

    def run(self):
        Handler = HTTPHandler
        socketserver.TCPServer.allow_reuse_address = True
        httpd = socketserver.TCPServer(("", self.PORT), Handler)
        httpd.serve_forever()


"""
REST API
"""


class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    def send_message(self, status, content_type, data):
        self.send_response(status)
        self.send_header("Content-type:", content_type)
        self.end_headers()
        self.wfile.write(data)
        self.wfile.write("\n".encode("utf-8"))

    def do_GET(self):
        """ Serve a GET request. """
        path = str(self.path).lstrip("/").split("?")[0]
        retval = API.calls.APIcall(path)
        if retval is not None:  # if call is valid API function
            try:
                args = str(self.path).lstrip("/").split("?")[1]
            except IndexError as e:
                print(e)
                self.send_message(403, "application/json", API.calls.jsonify({"error": "Missing parameters."}))
                return
            self.send_message(200, "application/json", retval(args))
        else:  # else parse as normal HTTP request
            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()

    def do_POST(self):
        """ Serve a POST request. """
        path = str(self.path).lstrip("/").split("?")[0]
        retval = API.calls.APIcall(path)
        if retval is not None:  # if call is valid API function
            try:
                args = str(self.path).lstrip("/").split("?")[1] #if no args
            except IndexError as e:
                print(e)
                self.send_message(403, "application/json", API.calls.jsonify({"error": "Missing parameters."}))
                return
            if self.headers["Content-Type"] == 'application/json':  # if data is json data
                length = int(self.headers["Content-Length"])
                rawdata = self.rfile.read(length)
                result = retval(args, API.calls.getfromrawjson(rawdata, "data"))
                self.send_message(200, "application/json", result)
            else:  # if not json data
                self.send_message(422, "application/json", API.calls.jsonify({"error": "Not JSON data."}))
        else:  # if not API function
            self.send_message(403, "application/json", API.calls.jsonify({"error": "Not an API function"}))
