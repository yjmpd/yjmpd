from flask import Blueprint, jsonify
from Database import get_database_instance
from YjmpdConfig import library_config

albumBlueprint = Blueprint('albumBlueprint', __name__)


@albumBlueprint.route('/')
def albums():
    db = get_database_instance()
    result = jsonify({"albums": db.execute_query_dict(
                        "SELECT albumName, COUNT(albumName) AS numberOfSongs, "
                        "albumArtist, albumCover, year, genre FROM tracks GROUP BY albumName;")
                      })
    db.disconnect()
    return result


@albumBlueprint.route('/<album_name>')
def album(album_name):
    album_name = album_name.replace('"', '\\"')
    album_name = album_name.replace("'", "\\'")
    db = get_database_instance()
    result = jsonify({"album": db.execute_query_dict(
                        "SELECT albumName, COUNT(albumName) AS numberOfSongs, "
                        "albumArtist, albumCover, year, genre FROM tracks WHERE albumName = '" +
                        album_name + "' GROUP BY albumName;")[0],
                      "songs": db.execute_query_dict(
                         "SELECT id, trackNumber, trackName, artistName, cdNumber, duration, year, genre, playCount,"
                         "CONCAT('"+library_config["public_path"]+"', SUBSTRING_INDEX(trackUrl,'"+library_config["library_path"]+"',-1)) as url "
                         "FROM tracks WHERE albumName = '" + album_name +
                         "' ORDER BY (cdNumber * 1), (trackNumber * 1) ASC;")
                      })
    db.disconnect()
    return result
