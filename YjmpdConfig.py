import configparser
import sys

http_config = {"port": 8585, "address": "127.0.0.1", "ssl": False, "privatekey": "", "certificate": ""}
database_config = {"port": 3306, "host": "127.0.0.1", "username": "", "password": "", "database": ""}
library_config = {"library_path": "", "public_path": ""}

def read_config(filename):
    config = configparser.ConfigParser()
    try:
        config.read(filename)
        http_config["port"] = config.getint("HTTP", "port")
        http_config["address"] = config.get("HTTP", "address")
        http_config["ssl"] = config.getboolean("HTTP", "ssl")
        http_config["privatekey"] = config.get("HTTP", "privatekey_file")
        http_config["certificate"] = config.get("HTTP", "certificate_file")

        database_config["port"] = config.getint("Database", "port")
        database_config["host"] = config.get("Database", "host")
        database_config["username"] = config.get("Database", "username")
        database_config["password"] = config.get("Database", "password")
        database_config["database"] = config.get("Database", "database")

        library_config["library_path"] = config.get("Library", "library_path")
        library_config["public_path"] = config.get("Library", "public_path")
    except Exception as e:
        print(e)
        sys.exit(1)
