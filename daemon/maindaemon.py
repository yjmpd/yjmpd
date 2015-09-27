import sys
import os
import configparser
from daemon.Database import Database
from daemon.libraryscanner import LibraryScanner
from daemon.yjmpd import YJMPD
from daemon.HTTPServer import HTTPServerThread

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
    db = Database(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
    LibraryScanner(db, MUSIC_DIR)
