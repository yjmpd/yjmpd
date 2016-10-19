import configparser
import os
import sys

from Database import Database
from YjmpdDaemon import YjmpdDaemon
from HTTPServer import HTTPServerThread
from api.API import API
from libraryscanner import LibraryScanner

config = configparser.ConfigParser()
try:
    config.read("config.cfg")
    HTTP_PORT = int(config.get("HTTP", "port"))
    HTTP_DOMAIN = str(config.get("HTTP", "domainname"))
    MUSIC_DIR = str(config.get("Library", "musicdir"))

    DB_USERNAME = config.get("Database", "username")
    DB_PASSWORD = config.get("Database", "password")
    DB_HOST = config.get("Database", "host")
    DB_DATABASE = config.get("Database", "database")
    DB_PORT = config.getint("Database", "port")

    CERT_FILE = config.get("HTTP", "cert")
except Exception as e:
    print(e)
    sys.exit(1)


class MainDaemon(YjmpdDaemon):
    def run(self):
        database = Database(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
        database2 = Database(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
        HTTPServerThread(HTTP_PORT, API(database, HTTP_DOMAIN + ":" + str(HTTP_PORT), MUSIC_DIR), MUSIC_DIR, CERT_FILE).start()
        LibraryScanner(database2, MUSIC_DIR)

if __name__ == "__main__":
    username = os.getenv('USER')
    if username is None:
        piddirectory = "/tmp/.yjmpddeamon.pid"
    else:
        piddirectory = "/home/" + username + "/.yjmpddeamon.pid"
    daemon = MainDaemon(piddirectory)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            os.chdir(MUSIC_DIR)
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        elif 'debug' == sys.argv[1]:
            database = Database(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
            http_thread = HTTPServerThread(HTTP_PORT, API(database, HTTP_DOMAIN + ":" + str(HTTP_PORT), MUSIC_DIR), MUSIC_DIR, CERT_FILE)
            http_thread.start()
            database2 = Database(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
            LibraryScanner(database2, MUSIC_DIR)
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|status|restart|debug" % sys.argv[0])
        sys.exit(2)
