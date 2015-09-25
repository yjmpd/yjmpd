import socket
import threading

endline = "\r\n"

class ServiceSocket(threading.Thread):
    def __init__(self, PORT):
        threading.Thread.__init__(self)
        self.PORT = PORT

    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(("", self.PORT))
        self.s.listen(1)
        while 1:
            conn, addr = self.s.accept()
            ClientHandler(conn).start()



class ClientHandler(threading.Thread):
    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.conn = conn
    def run(self):
        while 1:
            data = self.conn.recv(1024)
            if not data:
                break
            else:
                datastring = data.decode('utf-8', "ignore").rstrip(endline).lower()
                print(datastring)



