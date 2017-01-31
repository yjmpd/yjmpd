#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql
from YjmpdConfig import database_config
from warnings import filterwarnings
filterwarnings('ignore', category=pymysql.Warning)


def get_database_instance():
    return Database(database_config["username"], database_config["password"],
                    database_config["host"], database_config["port"], database_config["database"])


class Database:
    def __init__(self, db_username, db_password, db_host, db_port, db_database):
        self.cnx = pymysql.connect(user=db_username, password=db_password, host=db_host,
                                   database=db_database, port=db_port)
        self.dictCursor = self.cnx.cursor(pymysql.cursors.DictCursor)
        self.normalCursor = self.cnx.cursor()

    def disconnect(self):
        self.dictCursor.close()
        self.normalCursor.close()
        self.cnx.close()

    def turn_off_autocommit(self):
        self.execute_query_list("SET autocommit=0;")

    def execute_query_dict(self, query):
        try:
            self.dictCursor.execute(query)
            self.cnx.commit()
            fetch = self.dictCursor.fetchall()
            return fetch
        except pymysql.Error as e:
            print(e)
            return

    def execute_query_list(self, query, return_id=False):
        try:
            self.normalCursor.execute(query)
            self.cnx.commit()
            fetch = self.normalCursor.fetchall()
            if return_id:
                return self.normalCursor.lastrowid
            return fetch
        except pymysql.Error as e:
            print(e)
            return


def get_song_database_instance():
    return SongDatabase(database_config["username"], database_config["password"],
                        database_config["host"], database_config["port"], database_config["database"])


class SongDatabase(Database):
    buffer = []

    def remove_song(self, path):
        self.execute_query_list("DELETE FROM `tracks` WHERE trackUrl = " + path.replace("'", '\\\''))

    def insert_multiple_songs(self, genre, track_name, artist_name, album_name,
                              album_artist, track_number, disc_number, album_image,
                              year, duration, path):
        self.buffer.append([genre, track_name, artist_name, album_name,
                            album_artist, track_number, disc_number, album_image,
                            year, duration, path])
        if len(self.buffer) > 50:
            self.commit_buffer()

    def commit_buffer(self):
        query = 'INSERT INTO `tracks` (`genre`,`trackUrl`,`trackName`,`artistName`,`albumName`,`albumArtist`,' \
                '`trackNumber`, `cdNumber`, `albumCover`, `year`,`duration`) VALUES '
        for song in self.buffer:
            query += "("
            for field in song:
                query += "'" + field + "',"
            query = query[:-1]
            query += "),"
        query = query[:-1]
        query += " ON DUPLICATE KEY UPDATE `genre`=VALUES(`genre`) , `trackName` = VALUES(`trackName`) , " \
                 "`artistName` = VALUES(`artistName`) ,`albumName` = VALUES(`albumName`) , " \
                 "`albumArtist` = VALUES(`albumArtist`) , `trackNumber` = VALUES(`trackNumber`) , " \
                 "`cdNumber` = VALUES(`cdNumber`), `albumCover` = VALUES(`albumCover`), `year` = VALUES(`year`) , " \
                 "`duration` = VALUES(`duration`);"
        self.execute_query_list(query.encode())
        del self.buffer[:]
