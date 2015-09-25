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
            print(query)
            self.cursor.execute(query)
            self.cnx.commit()
        except pymysql.err.ProgrammingError as e:
            print(e)
            print(query)




