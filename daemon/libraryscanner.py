#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from mutagen.easyid3 import EasyID3
import mutagen._util
import os
import configparser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

config = configparser.ConfigParser()
config.read("../config.cfg")

class LibraryScanner:

    global url
    url = config.get("Library", "jancodir")
    def __init__(self, Database, librarypath):
        """Init class """
        self.url = librarypath
        self.db = Database

        ob = Observer()
        event = Filehandler(self)
        ob.schedule(event, url, recursive=True)
        ob.start()


    def scanRecursif(self):
        print("Scanning library "+url+" recursively...")
        i = 1
        query = ('INSERT INTO `tracks` (`genre`, `trackUrl`, `trackName`, `artistName`, `albumName`, `albumArtist`, `trackNumber`, `year`, `duration`) VALUES '.encode('utf8'))
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
        self.commitAndCleanQuery(query)


    def commitAndCleanQuery(self, query):
        query = query[:-1]
        query += b" ON DUPLICATE KEY UPDATE `genre`=VALUES(`genre`) , `trackName` = VALUES(`trackName`) , `artistName` = VALUES(`artistName`) ,`albumName` = VALUES(`albumName`) , `albumArtist` = VALUES(`albumArtist`) , `trackNumber` = VALUES(`trackNumber`) , `year` = VALUES(`year`) , `duration` = VALUES(`duration`)"
        self.db.executeQuery(query)
        return ('INSERT INTO `tracks` (`genre`, `trackUrl`, `trackName`, `artistName`, `albumName`, `albumArtist`, `trackNumber`, `year`, `duration`) VALUES '.encode('utf8'))

    def insertSong(self, path):
        try:
            id3 = EasyID3(path)
            self.db.executeQuery(b"INSERT INTO `tracks` (`genre`, `trackUrl`, `trackName`, `artistName`, `albumName`, `albumArtist`, `trackNumber`, `year`, `duration`) VALUES ('" + self.getValue(id3,"genre") + b"'," + b"'" + path.replace("'", '\\\'').encode('utf8') + b"'," + b"'" + self.getValue(id3, "title") + b"'," + b"'" + self.getValue(id3, "artist") + b"'," + b"'" +  self.getValue(id3, "album") + b"'," + b"'" +  self.getValue(id3, "performer") + b"'," + b"'" + self.getValue(id3, "tracknumber") + b"'," + b"'" + self.getValue(id3, "date") + b"'," + b"'0') "  +
                                 b" ON DUPLICATE KEY UPDATE `genre`=VALUES(`genre`) , `trackName` = VALUES(`trackName`) , `artistName` = VALUES(`artistName`) ,`albumName` = VALUES(`albumName`) , `albumArtist` = VALUES(`albumArtist`) , `trackNumber` = VALUES(`trackNumber`) , `year` = VALUES(`year`) , `duration` = VALUES(`duration`)")

        except: (mutagen.id3._util.ID3NoHeaderError)

    def removeSong(self,path):
        self.db.removeSong(path)

    def getValue(self, id3, value):
        try:
            return (id3[value][0].replace("'", '\\\'').encode('utf8'))
        except (KeyError,  IndexError, ValueError):
            print("Error reading value of ID3 tag",  end='\r')
        return b""


class Filehandler(FileSystemEventHandler):
    def __init__(self, LibraryScanner):
        self.libscanner = LibraryScanner

    def process(self, event):
        if not(event.is_directory):
            if os.path.isfile(event.src_path) and event.src_path.lower().endswith(('.mp3','.flac')):
                self.libscanner.insertSong(event.src_path)
            else:
                self.libscanner.removeSong(event.src_path)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)