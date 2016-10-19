#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql
from warnings import filterwarnings
filterwarnings('ignore', category=pymysql.Warning)


class Database:
    buffer = []

    def __init__(self, db_username, db_password, db_host, db_port, db_database):
        self.cnx = pymysql.connect(user=db_username, password=db_password, host=db_host,
                                   database=db_database, port=db_port)
        self.cursor = self.cnx.cursor()

    def executequery(self, query):
        try:
            self.cursor.execute(query)
            self.cnx.commit()
            return self.cursor.fetchall()
        except:
            self.cnx.connect()
            return self.executequery(query)

    def turnoffautocommit(self):
        self.executequery("SET autocommit=0;")

    def removesong(self, path):
        self.executequery("DELETE FROM `tracks` WHERE trackUrl = " + path.replace("'", '\\\''))

    def insertmultiplesongs(self, genre, trackname, artistname, albumname, albumartist, tracknumber, year, duration,
                            path):
        self.buffer.append([genre, trackname, artistname, albumname, albumartist, tracknumber, year, duration, path])
        if len(self.buffer) > 50:
            self.pushbuffer()

    def pushbuffer(self):
        query = 'INSERT INTO `tracks` (`genre`,`trackUrl`,`trackName`,`artistName`,`albumName`,`albumArtist`,`trackNumber`,`year`,`duration`) VALUES '
        for song in self.buffer:
            query += "("
            for field in song:
                query += "'" + field + "',"
            query = query[:-1]
            query += "),"
        query = query[:-1]
        query += " ON DUPLICATE KEY UPDATE `genre`=VALUES(`genre`) , `trackName` = VALUES(`trackName`) , `artistName` = VALUES(`artistName`) ,`albumName` = VALUES(`albumName`) , `albumArtist` = VALUES(`albumArtist`) , `trackNumber` = VALUES(`trackNumber`) , `year` = VALUES(`year`) , `duration` = VALUES(`duration`);"
        self.executequery(query.encode())
        del self.buffer[:]
