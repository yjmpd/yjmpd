#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import configparser
import pymysql
from warnings import filterwarnings


config = configparser.ConfigParser()
config.read("../config.cfg")
filterwarnings('ignore', category = pymysql.Warning)

class Database:

    def __init__(self):
        """Init class """
        self.cnx = pymysql.connect(user=config.get("Database", "username"), passwd=config.get("Database", "password"), host=config.get("Database", "host"), db=config.get("Database", "database"), port=config.getint("Database", "port"))
        self.cursor = self.cnx.cursor()

    def executeQuery(self, query):
        try:
            self.cursor.execute(query)
            self.cnx.commit()
        except (pymysql.err.ProgrammingError):
            print("something terrible wrong")




