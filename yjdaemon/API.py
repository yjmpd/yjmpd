import json

import configparser
"""
Add a key to the validAPIAPI dictionary, with a corresponding function
Function should return jsonified data, so that it can then be passed on to the client.
example:

Add this to the dictionary
"getsongs": API.getsongs

then implement this function
@staticmethod
    def getsongs():
        return API.jsonify({"song": song})

And the jsonified data will be returned to the client.

Every function MUST return jsonified data!

"""


class API:
    def __init__(self, DB):
        self.DB = DB
        self.validAPIcalls = {"getallsongs": self.getallsongs,
                 "setsong": self.setsong,
                 "getsongs": self.getsongs,
                 "getsongbyid": self.getsongbyid,
                 "getartists": self.getartists,
                 "getalbums": self.getalbums,
                 "getgenres": self.getgenres,
                 "getyears": self.getyears
                 }

    def APIcall(self,sanitizedpath):
        if sanitizedpath in self.validAPIcalls:
            return self.validAPIcalls[sanitizedpath]
        else:
            return None

    def getfromrawjson(self, data, param):
        return self.dejsonify(data)[param]

    def jsonify(self, data):
        return json.dumps(data, sort_keys=True, indent=4).encode("utf-8")

    def dejsonify(self, rawdata):
        return json.loads(rawdata.decode("utf-8"))

    def getallsongs(self, args):
        return self.jsonify({"songs": self.DB.executeQuery("SELECT * FROM tracks;"), "args": args , "result": "OK"})

    def getartists(self,args):
        return self.jsonify({"artists": self.DB.executeQuery("SELECT artistName FROM tracks GROUP BY artistName;"), "args": args, "result" : "OK"})

    def getalbums(self, args):
        return self.jsonify({"albums": self.DB.executeQuery("SELECT albumName FROM tracks GROUP BY albumName;"), "args": args, "result":"OK"})

    def getgenres(self, args):
        return self.jsonify({"genres": self.DB.executeQuery("SELECT genre FROM tracks GROUP BY genre;"), "args": args, "result":"OK"})

    def getyears(self, args):
        return self.jsonify({"years": self.DB.executeQuery("SELECT year FROM tracks GROUP BY year;"), "args": args, "result":"OK"})

    def getsongs(self, args):
        """Get song by album, genre, year, artist"""
        data = args.partition("?")
        splitstring = data[0].partition("=")
        print(splitstring)
        name= splitstring[0]
        value = splitstring[2].replace("%20"," ")
        if name == "album":
            songs = self.DB.executeQuery("SELECT * FROM tracks WHERE albumName = \"" + value + "\"")
        elif name == "genre":
            songs = self.DB.executeQuery("SELECT * FROM tracks WHERE genre = \"" + value + "\"")
        elif name == "year":
            songs = self.DB.executeQuery("SELECT * FROM tracks WHERE year = \"" + value + "\"")
        elif name == "artist":
            songs = self.DB.executeQuery("SELECT * FROM tracks WHERE artistName = \"" + value + "\"")
        else:
            return self.jsonify({"result":"NOK", "errormsg": "Not a valid argument"})
        return self.jsonify({"result":"OK","songs":songs})

    def getsongbyid(self, args):
        config = configparser.ConfigParser()
        try:
            config.read("config.cfg")
            musicdir = config.get("Library","musicdir")
            port = config.get("HTTP","port")
            domainname = config.get("HTTP","domainname")
        except:
            return self.jsonify({"result" : "NOK" , "errormsg" : "I/O error while reading config."})
        data = args.split("&")
        splitsting = data[0].split("=")
        id = splitsting[1]
        file = self.DB.executeQuery(
            "SELECT SUBSTRING_INDEX(trackUrl,'" + musicdir + "',-1) as filedir FROM `tracks` WHERE id = " + id)
        try:
            url = str(file[0][0])
        except:
            return self.jsonify({"result": "NOK", "errormsg" : "Song ID does not exist in database."})
        return self.jsonify({"result": "OK", "songurl": "http://"+domainname+":"+ port + url})

    def setsong(self, args, songname):
        global song
        song = songname
        return self.jsonify({"result": "OK", "args": args})

