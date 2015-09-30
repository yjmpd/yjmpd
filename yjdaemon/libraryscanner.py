#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from mutagen.easyid3 import EasyID3
import mutagen._util
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LibraryScanner:

    def __init__(self, Database, librarypath):
        """Init class """
        self.url = librarypath
        self.db = Database
        self.scanRecursif()
        ob = Observer()
        ob.schedule(Filehandler(self), self.url, recursive=True)
        ob.start()


    def scanRecursif(self):
        print("Scanning library "+self.url+" recursively...")
        # musicdirs = [os.path.join(self.url,o) for o in os.listdir(self.url) if os.path.isdir(os.path.join(self.url,o))]
        self.db.turnoffautocommit()
        for root, directories, filenames in os.walk(self.url):
            self.scandir(filenames,root)

    def scandir(self,filenames, root):
        for filename in filenames:
            if filename.lower().endswith(('.mp3','.flac',".m4a")):
                path = os.path.join(root,filename)
                try:
                    print(path, end='\r')
                    id3 = EasyID3(path)
                    self.db.insertMultipleSongs(self.getValue(id3, "genre"),path.replace("'", '\\\''),self.getValue(id3, "title"),self.getValue(id3, "artist"),self.getValue(id3, "album"),self.getValue(id3, "performer"),self.getValue(id3, "tracknumber"),self.getValue(id3, "date"),"0")
                except (mutagen.id3._util.ID3NoHeaderError):
                    print("Error reading ID3 tag",  end='\r')


    def insertSong(self, path):
        try:
            id3 = EasyID3(path)
            self.db.executeQuery(b"INSERT INTO `tracks` (`genre`, `trackUrl`, `trackName`, `artistName`, `albumName`, `albumArtist`, `trackNumber`, `year`, `duration`) VALUES ('" + self.getValue(id3,"genre") + b"'," + b"'" + path.replace("'", '\\\'').encode('utf8') + b"'," + b"'" + self.getValue(id3, "title") + b"'," + b"'" + self.getValue(id3, "artist") + b"'," + b"'" +  self.getValue(id3, "album") + b"'," + b"'" +  self.getValue(id3, "performer") + b"'," + b"'" + self.getValue(id3, "tracknumber") + b"'," + b"'" + self.getValue(id3, "date") + b"'," + b"'0') "  +
                                 b" ON DUPLICATE KEY UPDATE `genre`=VALUES(`genre`) , `trackName` = VALUES(`trackName`) , `artistName` = VALUES(`artistName`) ,`albumName` = VALUES(`albumName`) , `albumArtist` = VALUES(`albumArtist`) , `trackNumber` = VALUES(`trackNumber`) , `year` = VALUES(`year`) , `duration` = VALUES(`duration`)")

        except (mutagen.id3._util.ID3NoHeaderError):
            pass

    def removeSong(self,path):
        self.db.removeSong(path)

    def getValue(self, id3, value):
        try:
            return id3[value][0].replace("'", "\\'")
        except (KeyError,  IndexError, ValueError):
            print("Error reading value of ID3 tag",  end='\r')
        return ""


class Filehandler(FileSystemEventHandler):
    def __init__(self, LibraryScanner):
        self.libscanner = LibraryScanner

    def process(self, event):
        if not(event.is_directory):
            if os.path.isfile(event.src_path) and event.src_path.lower().endswith(('.mp3','.flac', 'm4a')):
                self.libscanner.insertSong(event.src_path)
            else:
                self.libscanner.removeSong(event.src_path)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)
