import decimal
import json


class API:

    def __init__(self, db, domain, musicdir):
        self.db = db
        self.domain = domain
        self.musicdir = musicdir
        self.validFilters = ["albumArtist", "albumName", "artistName", "trackName", "genre", "year"]

    """ Creates readable looking json """
    @staticmethod
    def jsonify(data):
        return json.dumps(data, default=API.decimal_default, sort_keys=True, indent=4).encode("utf-8")

    """ JSon to python list"""
    @staticmethod
    def dejsonify(rawdata):
        return json.loads(rawdata.decode("utf-8"))

    @staticmethod
    def decimal_default(obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        raise TypeError

    """ Creates a assocotive array with the given token name """
    @staticmethod
    def toassocotivearray(data, token):
        newdata = {}
        for row in data:
            if token in row:
                colname = row[token]
                del (row[token])
                if len(row) == 1:
                    newdata[colname] = next(iter(row.values()))
                else:
                    newdata[colname] = row
        return newdata

    def apicall(self, url, args, protocol):
        urlstrip = str(url).lstrip("/").split("/")
        if len(urlstrip) == 0:
            return self.jsonify("Missing parameters.")

        call = urlstrip[0]
        del urlstrip[0]

        if protocol == "get":
            if call == "artists":
                result = self.jsonify({"artists": self.db.executequerydict("SELECT artistName FROM tracks GROUP BY artistName;"), "result": "OK"})
            elif call == "albums":
                result = self.jsonify({"albums": self.db.executequerydict("SELECT albumName FROM tracks GROUP BY albumName;"), "result": "OK"})
            elif call == "years":
                result = self.jsonify({"years": self.db.executequerydict("SELECT year FROM tracks GROUP BY year;"), "result": "OK"})
            elif call == "genres":
                result = self.jsonify({"genres": self.db.executequerydict("SELECT genre FROM tracks GROUP BY genre;"), "result": "OK"})
            elif call == "songs":
                if len(urlstrip) > 0 and urlstrip[0] != "":
                    result = self.jsonify({"song": self.db.executequerydict("SELECT *, CONCAT('https://" + self.domain + "/', SUBSTRING_INDEX(trackUrl,'" + self.musicdir + "',-1)) as filedir FROM tracks WHERE id = " + urlstrip[0]), "result": "OK"})
                else:
                    filterstring = ""
                    for arg in args:
                        argsplit = arg.split("=", 1)
                        if len(argsplit) == 2 and argsplit[0] in self.validFilters:
                            filterstring += "AND " + argsplit[0] + "=\"" + argsplit[1] + "\""

                    result = self.jsonify({"songs": self.db.executequerydict("SELECT *, CONCAT('https://" + self.domain + "/', SUBSTRING_INDEX(trackUrl,'" + self.musicdir + "',-1)) as filedir FROM tracks WHERE 1=1 " + filterstring + ";"), "result": "OK"})
            else:
                result = False
        else:
            result = False

        return result

    def apigetcall(self, url, args):
        return self.apicall(url, args, "get")

    def apideletecall(self, url, args):
        return self.apicall(url, args, "delete")

    def apipostcall(self, url, args):
        try:
            args = self.dejsonify(args)
        except Exception as e:
            print(e)
            return API.jsonify({"error": "Error while parsing content json"})
        return self.apicall(url, args, "post")

    def apiputcall(self, url, args):
        try:
            args = self.dejsonify(args)
        except Exception as e:
            print(e)
            return self.jsonify({"error": "Error while parsing content json"})
        return self.apicall(url, args, "put")

