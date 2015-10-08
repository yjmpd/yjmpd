import json
from yjdaemon.Database import Database

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
        return calls.jsonify({"song": song, "args": args})

    @staticmethod
    def setsong(args, songname):
        global song
        song = songname
        return calls.jsonify({"result": "OK", "args": args})


validAPIcalls = {"getsongs": calls.getsongs, "setsong": calls.setsong}
song = "HALLO"
