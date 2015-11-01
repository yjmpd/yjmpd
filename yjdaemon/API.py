import json

from yjdaemon.Database import Database as db
import configparser
"""
Add a key to the validAPIcalls dictionary, with a corresponding function
Function should return jsonified data, so that it can then be passed on to the client.
example:

Add this to the dictionary
"getsongs": calls.getsongs

then implement this function
@staticmethod
    def getsongs():
        return calls.jsonify({"song": song})

And the jsonified data will be returned to the client.

Every function MUST return jsonified data!

"""


class calls:
    @staticmethod
    def APIcall(sanitizedpath):
        if sanitizedpath in validAPIcalls:
            return validAPIcalls[sanitizedpath]
        else:
            return None

    @staticmethod
    def getfromrawjson(data, param):
        return calls.dejsonify(data)[param]

    @staticmethod
    def jsonify(data):
        return json.dumps(data, sort_keys=True, indent=4).encode("utf-8")

    @staticmethod
    def dejsonify(rawdata):
        return json.loads(rawdata.decode("utf-8"))

    @staticmethod
    def getallsongs(args):
        return calls.jsonify({"songs": db.executequerystatic("SELECT * FROM tracks;"), "args": args , "result": "OK"})

    @staticmethod
    def getartists(args):
        return calls.jsonify({"artists": db.executequerystatic("SELECT artistName FROM tracks GROUP BY artistName;"), "args": args, "result" : "OK"})

    @staticmethod
    def getalbums(args):
        return calls.jsonify({"albums": db.executequerystatic("SELECT albumName FROM tracks GROUP BY albumName;"), "args": args, "result":"OK"})

    @staticmethod
    def getgenres(args):
        return calls.jsonify({"genres": db.executequerystatic("SELECT genre FROM tracks GROUP BY genre;"), "args": args, "result":"OK"})

    @staticmethod
    def getyears(args):
        return calls.jsonify({"years": db.executequerystatic("SELECT year FROM tracks GROUP BY year;"), "args": args, "result":"OK"})

    @staticmethod
    def getsongs(args):
        """Get song by album, genre, year, artist"""
        data = args.partition("?")
        splitstring = data[0].partition("=")
        print(splitstring)
        name= splitstring[0]
        value = splitstring[2].replace("%20"," ")
        if name == "album":
            songs = db.executequerystatic("SELECT * FROM tracks WHERE albumName = \"" + value + "\"")
        elif name == "genre":
            songs = db.executequerystatic("SELECT * FROM tracks WHERE genre = \"" + value + "\"")
        elif name == "year":
            songs = db.executequerystatic("SELECT * FROM tracks WHERE year = \"" + value + "\"")
        elif name == "artist":
            songs = db.executequerystatic("SELECT * FROM tracks WHERE artistName = \"" + value + "\"")
        else:
            return calls.jsonify({"result":"NOK", "errormsg": "Not a valid argument"})
        return calls.jsonify({"result":"OK","songs":songs})

    @staticmethod
    def getsongbyid(args):
        config = configparser.ConfigParser()
        try:
            config.read("config.cfg")
            musicdir = config.get("Library","musicdir")
            port = config.get("HTTP","port")
            domainname = config.get("HTTP","domainname")
        except:
            return calls.jsonify({"result" : "NOK" , "errormsg" : "I/O error while reading config."})
        data = args.split("&")
        splitsting = data[0].split("=")
        id = splitsting[1]
        file = db.executequerystatic(
            "SELECT SUBSTRING_INDEX(trackUrl,'" + musicdir + "',-1) as filedir FROM `tracks` WHERE id = " + id)
        try:
            url = str(file[0][0])
        except:
            return calls.jsonify({"result": "NOK", "errormsg" : "Song ID does not exist in database."})
        return calls.jsonify({"result": "OK", "songurl": "http://"+domainname+":"+ port + url})

    @staticmethod
    def setsong(args, songname):
        global song
        song = songname
        return calls.jsonify({"result": "OK", "args": args})


validAPIcalls = {"getallsongs": calls.getallsongs,
                 "setsong": calls.setsong,
                 "getsongs": calls.getsongs,
                 "getsongbyid": calls.getsongbyid,
                 "getartists": calls.getartists,
                 "getalbums": calls.getalbums,
                 "getgenres": calls.getgenres,
                 "getyears": calls.getyears
                 }
