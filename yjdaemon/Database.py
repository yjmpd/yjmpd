#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql
from threading import RLock as Lock
from warnings import filterwarnings

filterwarnings('ignore', category = pymysql.Warning)
class Database:

    buffer = []
    cout = 0
    lock = Lock()
    def __init__(self, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE):
        """Init class """
        self.cnx = pymysql.connect(user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST,  database=DB_DATABASE, port=DB_PORT)
        self.cursor = self.cnx.cursor()

    def executeQuery(self, query):
        try:
            self.cursor.execute(query)
            self.cnx.commit()
            return self.cursor.fetchall()
        except pymysql.err.ProgrammingError as e:
            print(e)
            print(query)

    def turnoffautocommit(self):
        self.cursor.execute("SET autocommit=0;")
        self.cnx.commit()

    def removeSong(self, path):
         self.db.executeQuery("DELETE FROM `tracks` WHERE trackUrl = " + path.replace("'", '\\\''))

    def updateInsertSong(self, genre, trackname, artistname, albumname, albumartist, tracknumber, year, duration, path): #notworking
        self.db.executeQuery("INSERT INTO `tracks` (`genre`, `trackUrl`, `trackName`, `artistName`, `albumName`, `albumArtist`, `trackNumber`, `year`, `duration`) VALUES ('" + genre + b"','" + path.replace("'", '\\\'') + "','" + trackname + "','" + artistname + "','" + albumname + "','" + albumartist + "','" + tracknumber + "','" + year + "','0') " +
                             b" ON DUPLICATE KEY UPDATE `genre`=VALUES(`genre`) , `trackName` = VALUES(`trackName`) , `artistName` = VALUES(`artistName`) ,`albumName` = VALUES(`albumName`) , `albumArtist` = VALUES(`albumArtist`) , `trackNumber` = VALUES(`trackNumber`) , `year` = VALUES(`year`) , `duration` = VALUES(`duration`)")

    def insertMultipleSongs(self, genre, trackname, artistname, albumname, albumartist, tracknumber, year, duration, path):
        self.buffer.append([genre, trackname, artistname, albumname, albumartist, tracknumber, year, duration, path])
        # Database.lock.acquire()
        if len(self.buffer) > 50:
            self.pushbuffer()
        # Database.lock.release()

    def pushbuffer(self):
        query = ('INSERT INTO `tracks` (`genre`, `trackUrl`, `trackName`, `artistName`, `albumName`, `albumArtist`, `trackNumber`, `year`, `duration`) VALUES ')
        for song in self.buffer:
            query += "("
            for field in song:
                query += "'" + field + "',"
            query = query[:-1]
            query += "),"
        query = query[:-1]
        query += " ON DUPLICATE KEY UPDATE `genre`=VALUES(`genre`) , `trackName` = VALUES(`trackName`) , `artistName` = VALUES(`artistName`) ,`albumName` = VALUES(`albumName`) , `albumArtist` = VALUES(`albumArtist`) , `trackNumber` = VALUES(`trackNumber`) , `year` = VALUES(`year`) , `duration` = VALUES(`duration`);"
        self.executeQuery(query.encode())
        del self.buffer[:]

