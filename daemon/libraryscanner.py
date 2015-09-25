#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from mutagen.easyid3 import EasyID3
import mutagen._util
import os
import configparser
from Database import Database
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

config = configparser.ConfigParser()
config.read("../config.cfg")

class LibraryScanner:

    global url
    url = config.get("Library", "jancodir")
    def __init__(self):
        """Init class """
        ob = Observer()
        event = Filehandler()
        ob.schedule(event, url, recursive=True)
        ob.start()
        self.db = Database()

    def scanRecursif(self):
        print("Scanning library "+url+" recursifly...")
        i = 1
        query = ('REPLACE INTO `tracks` (`genre`, `trackUrl`, `trackName`, `artistName`, `albumName`, `albumArtist`, `trackNumber`, `year`, `duration`) VALUES '.encode('utf8'))
        for root, directories, filenames in os.walk(url):
            for filename in filenames:
                if filename.lower().endswith(('.mp3','.flac')):
                    if(i % 50 == 0 ):
                        query = self.commitAndCleanQuery(query)
                    path = os.path.join(root,filename)
                    i+=1
                    try:
                        print(str(i) + '\t' + path, end='\r')
                        id3 = EasyID3(path)
                        query += (b"('" + self.getValue(id3,"genre") + b"'," + b"'" + path.replace("'", '\\\'').encode('utf8') + b"'," + b"'" + self.getValue(id3, "title") + b"'," + b"'" +  self.getValue(id3, "artist") + b"'," + b"'" +  self.getValue(id3, "album") + b"'," + b"'" +  self.getValue(id3, "performer") + b"'," + b"'" +  self.getValue(id3, "tracknumber") + b"'," + b"'" +  self.getValue(id3, "date") + b"'," + b"'0'),")
                    except (mutagen.id3._util.ID3NoHeaderError):
                        print("Error reading ID3 tag",  end='\r')


    def commitAndCleanQuery(self, query):
        query = query[:-1]
        query += (';'.encode('utf8'))
        self.db.executeQuery(query)
        return ('REPLACE INTO `tracks` (`genre`, `trackUrl`, `trackName`, `artistName`, `albumName`, `albumArtist`, `trackNumber`, `year`, `duration`) VALUES '.encode('utf8'))

    def getValue(self, id3, value):
        try:
            return (id3[value][0].replace("'", '\\\'').encode('utf8'))
        except (KeyError,  IndexError, ValueError):
            print("Error reading value of ID3 tag",  end='\r')
        return "".encode('utf8')


class Filehandler(FileSystemEventHandler):
    def on_modified(self, event):
        print (event) 

if __name__ == "__main__":
    try:
        libscanner = LibraryScanner()
        libscanner.scanRecursif()
    except KeyboardInterrupt:
        print("Bye")


