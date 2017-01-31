#!/usr/bin/env python3
from Api import Api
from YjmpdConfig import read_config
from Libraryscanner import LibraryScanner


if __name__ == "__main__":
    read_config("config.cfg")
    LibraryScanner()
    Api()
