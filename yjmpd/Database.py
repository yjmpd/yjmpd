#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql
from warnings import filterwarnings
filterwarnings('ignore', category=pymysql.Warning)


class Database:
    buffer = []

    def __init__(self, db_username, db_password, db_host, db_port, db_database):
        self.username = db_username
        self.password = db_password
        self.host = db_host
        self.port = db_port
        self.database = db_database

        self.cnx = pymysql.connect(user=db_username, password=db_password, host=db_host,
                                   database=db_database, port=db_port)
        self.dictCursor = self.cnx.cursor(pymysql.cursors.DictCursor)
        self.normalcursor = self.cnx.cursor()

    def disconnect(self):
        self.dictCursor.close()
        self.normalcursor.close()
        self.cnx.close()

    def turnoffautocommit(self):
        self.executequerylist("SET autocommit=0;")

    def getinstance(self):
        return Database(self.username, self.password, self.host, self.port, self.database)

    def executequerydict(self, query):
        try:
            self.dictCursor.execute(query)
            self.cnx.commit()
            fetch = self.dictCursor.fetchall()
            return fetch
        except pymysql.Error as e:
            print(e)
            return

    def executequerylist(self, query, returnid=False):
        try:
            self.normalcursor.execute(query)
            self.cnx.commit()
            fetch = self.normalcursor.fetchall()
            if returnid:
                return self.normalcursor.lastrowid
            return fetch
        except pymysql.Error as e:
            print(e)
            return

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
        self.executequerylist(query.encode())
        del self.buffer[:]
