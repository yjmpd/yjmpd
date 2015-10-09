import json

from yjdaemon.Database import Database as db
from yjdaemon.maindaemon import MUSIC_DIR

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
    def getsongs(args):
        return calls.jsonify({"songs": db.executequerystatic("SELECT id, trackName FROM tracks;"), "args": args})

    @staticmethod
    def getartists(args):
        return calls.jsonify({"artists": db.executequerystatic("SELECT artistName FROM tracks GROUP BY artistName;"), "args": args})   @staticmethod

    @staticmethod
    def getalbums(args):
        return calls.jsonify({"albums": db.executequerystatic("SELECT albumName FROM tracks GROUP BY albumName;"), "args": args})

    @staticmethod
    def getgenres(args):
        return calls.jsonify({"genres": db.executequerystatic("SELECT genre FROM tracks GROUP BY genre;"), "args": args})

    @staticmethod
    def getyears(args):
        return calls.jsonify({"years": db.executequerystatic("SELECT year FROM tracks GROUP BY year;"), "args": args})

    @staticmethod
    def getalbumnames(args):
        return calls.jsonify({"albumnames": db.executequerystatic("SELECT albumName FROM tracks GROUP BY albumName;"), "args": args})

    @staticmethod
    def getsongbyid(args):
        data = args.split("&")
        splitsting = data[0].split("=")
        id = splitsting[1]
        file = db.executequerystatic(
            "SELECT SUBSTRING_INDEX(trackUrl,'" + MUSIC_DIR + "',-1) as filedir FROM `tracks` WHERE id = " + id)
        try:
            url = str(file[0][0])
        except:
            return calls.jsonify({"result": "NOK", "errormsg" : "Song ID does not exist in database."})
        return calls.jsonify({"result": "OK", "songurl": "http://localhost:8585/" + url})

    @staticmethod
    def setsong(args, songname):
        global song
        song = songname
        return calls.jsonify({"result": "OK", "args": args})


validAPIcalls = {"getsongs": calls.getsongs,
                 "setsong": calls.setsong,
                 "getsongbyid": calls.getsongbyid,
                 "getartists": calls.getartists,
                 "getalbums": calls.getalbums,
                 "getgenres": calls.getgenres,
                 "getyears": calls.getyears,
                 "getalbumnames": calls.getalbumnames
                 }
