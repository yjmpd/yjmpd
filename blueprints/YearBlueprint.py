from flask import Blueprint, jsonify
from Database import get_database_instance
from YjmpdConfig import library_config

yearBlueprint = Blueprint('yearBlueprint', __name__)


@yearBlueprint.route('/')
def years():
    db = get_database_instance()
    result = jsonify({"years": db.execute_query_dict(
                        "SELECT year, COUNT(year) AS numberOfSongs FROM tracks GROUP BY year;")
                      })
    db.disconnect()
    return result


@yearBlueprint.route('/<year>')
def album(year):
    year = year.replace('"', '\\"')
    year = year.replace("'", "\\'")
    db = get_database_instance()
    result = jsonify({"year": db.execute_query_dict(
                        "SELECT year, COUNT(year) AS numberOfSongs FROM tracks "
                        "WHERE year = '" + year + "' GROUP BY year;")[0],
                      "albums": db.execute_query_dict(
                        "SELECT albumName, COUNT(albumName) AS numberOfSongs, "
                        "albumArtist, albumCover, year, genre FROM tracks WHERE year = '" +
                        year + "' GROUP BY albumName;"),
                      "songs": db.execute_query_dict(
                         "SELECT id, trackNumber, trackName, artistName, cdNumber, duration, year, genre, playCount,"
                         "CONCAT('"+library_config["public_path"]+"', SUBSTRING_INDEX(trackUrl,'"+library_config["library_path"]+"',-1)) as url "
                         "FROM tracks WHERE year = '" + year +
                         "' ORDER BY (cdNumber * 1), (trackNumber * 1) ASC;")
                      })
    db.disconnect()
    return result
