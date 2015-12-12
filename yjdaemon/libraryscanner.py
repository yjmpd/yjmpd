#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import mutagen._util
import os
from mutagen import File
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class LibraryScanner:
    def __init__(self, db, librarypath):
        self.url = librarypath
        self.db = db
        self.scanrecursif()
        ob = Observer()
        ob.schedule(Filehandler(self), self.url, recursive=True)
        ob.start()

    def scanrecursif(self):
        self.db.turnoffautocommit()
        if not os.path.exists(os.path.join(self.url, ".artwork")):
            os.makedirs(os.path.join(self.url, ".artwork"))
        for root, directories, filenames in os.walk(self.url):
            self.scandir(filenames,root)

    def scandir(self, filenames, root):
        for filename in filenames:
            if filename.lower().endswith(('.mp3', '.flac', '.m4a')):
                path = os.path.join(root, filename)
                try:
                    print(path, end='\r')
                    id3 = EasyID3(path)
                    audio = MP3(path)
                    albumname = self.getvalue(id3, "album")
                    if albumname is "":
                        albumname = "default"
                    if not os.path.isfile(os.path.join(self.url, ".artwork/" + albumname + ".jpg")):
                        try:
                            file = File(path)
                            artwork = file.tags['APIC:'].data
                            with open(os.path.join(self.url, ".artwork/" + self.getvalue(id3, "album") + ".jpg"), 'wb') as img:
                                img.write(artwork)
                        except:
                            print('Artwork error on album:' + self.getvalue(id3, "album"))
                    self.db.insertmultiplesongs(self.getvalue(id3, "genre"), path.replace("'", '\\\''),
                                                self.getvalue(id3, "title"), self.getvalue(id3, "artist"),
                                                self.getvalue(id3, "album"), self.getvalue(id3, "performer"),
                                                self.getvalue(id3, "tracknumber"), self.getvalue(id3, "date"),
                                                str(audio.info.length))
                except mutagen.id3._util.ID3NoHeaderError:
                    print("Error reading ID3 tag",  end='\r')

    def insertsong(self, path):
        try:
            id3 = EasyID3(path)
            query = """
            INSERT INTO `tracks` (`genre`, `trackUrl`, `trackName`, `artistName`, `albumName`, `albumArtist`, `trackNumber`, `year`, `duration`)
            VALUES ('%s', '%s','%s','%s','%s','%s','%s','%s','%s','0')
            ON DUPLICATE KEY UPDATE
            `genre`=VALUES(`genre`) , `trackName` = VALUES(`trackName`) , `artistName` = VALUES(`artistName`) ,
            `albumName` = VALUES(`albumName`) , `albumArtist` = VALUES(`albumArtist`) , `trackNumber` = VALUES(`trackNumber`) ,
             `year` = VALUES(`year`) , `duration` = VALUES(`duration`)"
            """ % (self.getvalue(id3, "genre"), path.replace("'", '\\\''), self.getvalue(id3, "title"), self.getvalue(id3, "artist"),
                   self.getvalue(id3, "album"), self.getvalue(id3, "performer"), self.getvalue(id3, "tracknumber"), self.getvalue(id3, "date"), self.getvalue(id3, ""))
            print(query)
            self.db.executequery(query)
        except (mutagen.id3._util.ID3NoHeaderError):
            pass

    def removesong(self, path):
        self.db.removesong(path)

    def getvalue(self, id3, value):
        try:
            return id3[value][0].replace("'", "\\'")
        except (KeyError,  IndexError, ValueError):
            print("Error reading value of ID3 tag",  end='\r')
        return ""


class Filehandler(FileSystemEventHandler):
    def __init__(self, libraryscanner):
        self.libscanner = libraryscanner

    def process(self, event):
        if not event.is_directory:
            if os.path.isfile(event.src_path) and event.src_path.lower().endswith(('.mp3','.flac', 'm4a')):
                self.libscanner.insertsong(event.src_path)
            else:
                self.libscanner.removesong(event.src_path)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)
