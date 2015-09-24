import sys
import os
from daemon.yjmpd import YJMPD
from daemon.HTTPServer import HTTPServerThread

debug = False

HTTP_PORT = 8585 #Get this from config
MUSIC_DIR = "" #Get this from config

class MainDaemon(YJMPD):
    def run(self):
        HTTP_thread = HTTPServerThread(HTTP_PORT)
        HTTP_thread.start()


if __name__ == "__main__":
    username = os.getenv('USER')
    if None == username:
        dir = "/tmp/.pydaemon.pid"
    else:
        dir = "/home/" + username + "/.pydaemon.pid"
    daemon = MainDaemon(dir, MUSIC_DIR)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|status|restart" % sys.argv[0])
        sys.exit(2)
