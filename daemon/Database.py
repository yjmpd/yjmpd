#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import configparser
import pymysql
from warnings import filterwarnings

filterwarnings('ignore', category = pymysql.Warning)
class Database:

    def __init__(self, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE):
        """Init class """
        self.cnx = pymysql.connect(user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST,  database=DB_DATABASE, port=DB_PORT)
        self.cursor = self.cnx.cursor()

    def executeQuery(self, query):
        try:
            self.cursor.execute(query)
            self.cnx.commit()
        except pymysql.err.ProgrammingError as e:
            print(e)
            print(query)

    def removeSong(self, path):
         self.db.executeQuery("DELETE FROM `tracks` WHERE trackUrl = " + path.replace("'", '\\\''))

    def updateInsertSong(self, genre, trackname, artistname, albumname, albumartist, tracknumber, year, duration, path): #notworking
        self.db.executeQuery("INSERT INTO `tracks` (`genre`, `trackUrl`, `trackName`, `artistName`, `albumName`, `albumArtist`, `trackNumber`, `year`, `duration`) VALUES ('" + genre + b"','" + path.replace("'", '\\\'') + "','" + trackname + "','" + artistname + "','" + albumname + "','" + albumartist + "','" + tracknumber + "','" + year + "','0') " +
                             b" ON DUPLICATE KEY UPDATE `genre`=VALUES(`genre`) , `trackName` = VALUES(`trackName`) , `artistName` = VALUES(`artistName`) ,`albumName` = VALUES(`albumName`) , `albumArtist` = VALUES(`albumArtist`) , `trackNumber` = VALUES(`trackNumber`) , `year` = VALUES(`year`) , `duration` = VALUES(`duration`)")


