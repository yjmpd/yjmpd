#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from mutagen.easyid3 import EasyID3
import mutagen._util
import os
import configparser

config = configparser.ConfigParser()
config.read("config.cfg")
print(config.sections())

class LibraryScanner:

    global url
    #url="/mnt/Muziek/" #TODO: moet gelezen worden vanaf config. Maybe static class met config paramaters zodat alle klasses deze kunnen inzien?
    url = config.get("Library", "jancodir")
    def __init__(self):
        """Init class """

    def scanRecursif(self):
        for root, directories, filenames in os.walk(url):
            for filename in filenames:
                if filename.lower().endswith(('.mp3','.flac')):
                    path = os.path.join(root,filename)
                    try:
                        id3 = EasyID3(path)
                        try:
                            print (id3);
                            print("%s \t\t %s \t\t %s" % (self.getValue(id3,"title"), self.getValue(id3, "genre"), self.getValue(id3, "performer'")))
                        except KeyError:
                            print("something wrong with this value")
                    except (mutagen.id3._util.ID3NoHeaderError):
                        print("Fuck deze id3 tag")

    def getValue(self, id3, value):
        try:
            return (id3[value][0].encode('utf8'))
        except (KeyError,  IndexError):
            print("error")
        return "";


if __name__ == "__main__":
    try:
        libscanner = LibraryScanner()
        libscanner.scanRecursif()

    except KeyboardInterrupt:
        print("Bye")