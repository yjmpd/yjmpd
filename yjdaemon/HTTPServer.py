#!/usr/bin/env python3


import http.server
import socketserv as socketserv
import threading
import html

"""
HTTP request handler.
"""


class HTTPServerThread(threading.Thread):
    def __init__(self, PORT, API):
        threading.Thread.__init__(self)
        self.PORT = PORT
        self.API = API

    def run(self):
        Handler = HTTPHandler
        socketserv.TCPServer.allow_reuse_address = True
        httpd = socketserv.TCPServer(("", self.PORT), Handler, self.API)
        httpd.serve_forever()


"""
REST API
"""


class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,request, client_address, server):
        self.api = server.api
        http.server.SimpleHTTPRequestHandler.__init__(self, request,client_address,server)



    def send_message(self, status, content_type, data):
        self.send_response(status)
        self.send_header("Content-type:", content_type)
        self.end_headers()
        self.wfile.write(data)
        self.wfile.write("\n".encode("utf-8"))

    def do_GET(self):
        """ Serve a GET request. """
        path = html.unescape(self.path)
        path = str(path).lstrip("/").split("?")[0]
        retval = self.api.apicall(path)
        print(path)
        if retval is not None:  # if call is valid API function
            try:
                args = str(html.unescape(self.path)).lstrip("/").split("?")[1]
            except IndexError as e:
                print(e)
                self.send_message(403, "application/json", self.api.jsonify({"error": "Missing parameters."}))
                return
            print(args)
            self.send_message(200, "application/json", retval( args))
        else:  # else parse as normal HTTP request
            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()

    def do_POST(self):
        """ Serve a POST request. """
        path = html.unescape(self.path)
        path = str(path).lstrip("/").split("?")[0]
        retval = self.api.apicall(path)
        if retval is not None:  # if call is valid API function
            try:
                args = str(html.unescape(self.path)).lstrip("/").split("?")[1] #if no args
            except IndexError as e:
                print(e)
                self.send_message(403, "application/json", self.api.jsonify({"error": "Missing parameters."}))
                return
            if self.headers["Content-Type"] == 'application/json':  # if data is json data
                length = int(self.headers["Content-Length"])
                rawdata = self.rfile.read(length)
                result = retval(args, self.api.getfromrawjson(rawdata, "data"))
                self.send_message(200, "application/json", result)
            else:  # if not json data
                self.send_message(422, "application/json", self.api.jsonify({"error": "Not JSON data."}))
        else:  # if not API function
            self.send_message(403, "application/json", self.api.jsonify({"error": "Not an API function"}))
