import sys
import os
import configparser
from yjdaemon.Database import Database
from yjdaemon.libraryscanner import LibraryScanner
from yjdaemon.yjmpd import YJMPD
from yjdaemon.HTTPServer import HTTPServerThread

debug = False

config = configparser.ConfigParser()
try:
    config.read("../config.cfg")
    HTTP_PORT = int(config.get("HTTP", "port"))
    DAEMON_PORT = int(config.get("Daemon", "port"))
    MUSIC_DIR = str(config.get("Library", "jancodir"))

    DB_USERNAME = config.get("Database", "username")
    DB_PASSWORD = config.get("Database", "password")
    DB_HOST     = config.get("Database", "host")
    DB_DATABASE = config.get("Database", "database")
    DB_PORT     = config.getint("Database", "port")

except Exception as e:
    print(e.with_traceback())
    sys.exit(1)


class MainDaemon(YJMPD):
    def run(self):
        HTTP_thread = HTTPServerThread(HTTP_PORT)
        HTTP_thread.start()
        db = Database(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
        LibraryScanner(db, MUSIC_DIR)



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
