#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import mutagen._util
import os
import re
from PIL import Image
from mutagen import File
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from YjmpdConfig import library_config
import unicodedata
from Database import get_song_database_instance


class LibraryScanner(threading.Thread):
    valid_extentions = ('.mp3', '.flac', '.m4a')

    def __init__(self):
        threading.Thread.__init__(self)
        self.library_path = library_config["library_path"]
        self.start()

    def run(self):
        self.scan_recursively()
        ob = Observer()
        ob.schedule(FileHandler(self), self.library_path, recursive=True)
        ob.start()

    def scan_recursively(self):
        db = get_song_database_instance()
        db.turn_off_autocommit()
        if not os.path.exists(os.path.join(self.library_path, ".artwork")):
            os.makedirs(os.path.join(self.library_path, ".artwork"))
        for root, directories, files in os.walk(self.library_path):
            self.scan_directory(files, root, db)

    def scan_directory(self, files, root, db):
        print("Scanning directory: " + root)
        for filename in files:
            if filename.lower().endswith(self.valid_extentions):
                path = os.path.join(root, filename)
                self.scan_song(path, db)

    def scan_song(self, song_path, db):
        try:
            id3 = EasyID3(song_path)
            audio = MP3(song_path)

            album_name = self.get_id3_value(id3, "album")
            album_cover_name = self.slugify(album_name) + ".jpg"
            track_number = self.get_id3_value(id3, "tracknumber")
            disc_number = self.get_id3_value(id3, "discnumber")
            title = self.get_id3_value(id3, "title")
            artist = self.get_id3_value(id3, "artist")
            genre = self.get_id3_value(id3, "genre")
            album_artist = self.get_id3_value(id3, "albumartist")
            duration = str(audio.info.length)
            year = self.get_id3_value(id3, "date")
            safe_path = song_path.replace("'", '\\\'')

            if "/" in track_number:
                track_number = track_number.partition("/")[0]
            if "/" in disc_number:
                disc_number = disc_number.partition("/")[0]
            if not os.path.isfile(os.path.join(self.library_path, ".artwork/" + album_cover_name)):
                try:
                    file = File(song_path)
                    artwork = ""
                    for key in file:
                        if key.startswith("APIC:"):
                            artwork = file.tags[key].data
                    if artwork == "":
                        artwork = file["APIC:"].data
                    url = os.path.join(self.library_path, ".artwork/tmp.jpg")
                    with open(url, 'wb') as img:
                        img.write(artwork)
                    artwork_image = Image.open(url)
                    artwork_image = artwork_image.resize((150, 150), Image.ANTIALIAS)
                    artwork_image.save(
                        os.path.join(self.library_path, ".artwork/" + album_cover_name),
                        quality=40)
                except:
                    print('Artwork error on album:' + self.get_id3_value(id3, "album"), end='\r')
                    album_cover_name = "default"
            db.insert_multiple_songs(genre, safe_path, title, artist, album_name, album_artist,
                                     track_number, disc_number, album_cover_name, year, duration)
        except mutagen.id3._util.ID3NoHeaderError:
            print("Error reading ID3 tag: " + song_path)

    @staticmethod
    def get_id3_value(id3, value):
        try:
            return id3[value][0].replace("'", "\\'")
        except (KeyError,  IndexError, ValueError):
            return ""

    @staticmethod
    def slugify(value):
        slug = unicodedata.normalize('NFKD', value)
        slug = slug.encode('ascii', 'ignore').lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug.decode('ascii')).strip('-')
        slug = re.sub(r'[-]+', '-', slug)
        return slug


class FileHandler(FileSystemEventHandler):
    def __init__(self, library_scanner):
        self.library_scanner = library_scanner

    def process(self, event):
        if not event.is_directory:
            db = get_song_database_instance()
            if os.path.isfile(event.src_path) and event.src_path.lower().endswith(self.library_scanner.valid_extentions):
                self.library_scanner.scan_song(event.src_path, db)
            else:
                db.remove_song(event.src_path)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)
