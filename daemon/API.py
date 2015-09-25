import json


class calls:
    @staticmethod
    def APIcall(sanitizedpath, type):
        if type == "get":
            if sanitizedpath in validAPIcalls:
                return validAPIcalls[sanitizedpath]()
            else:
                return None
        elif type == "post":
            if sanitizedpath in validAPIcalls:
                return validAPIcalls[sanitizedpath]
            else:
                return None

    @staticmethod
    def getfromjson(data, param):
        return calls.dejsonify(data)[param]

    @staticmethod
    def jsonify(data):
        return json.dumps(data, sort_keys=True, indent=4).encode("utf-8")

    @staticmethod
    def dejsonify(rawdata):
        return json.loads(rawdata.decode("utf-8"))

    @staticmethod
    def getsongs():
        return calls.jsonify({"song": song})

    @staticmethod
    def setsong(songname):
        global song
        song = songname
        return calls.jsonify({"result": "OK"})


validAPIcalls = {"getsongs": calls.getsongs, "setsong": calls.setsong}
song = "HALLO"
