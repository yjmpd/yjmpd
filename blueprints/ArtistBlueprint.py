from flask import Blueprint, jsonify
from Database import get_database_instance
from YjmpdConfig import library_config

artistBlueprint = Blueprint('artistBlueprint', __name__)


@artistBlueprint.route('/')
def artists():
    db = get_database_instance()
    result = jsonify({"artists": db.execute_query_dict(
                        "SELECT artistName, COUNT(artistName) AS numberOfSongs FROM tracks GROUP BY artistName;")
                      })
    db.disconnect()
    return result


@artistBlueprint.route('/<artist_name>')
def artist(artist_name):
    artist_name = artist_name.replace('"', '\\"')
    artist_name = artist_name.replace("'", "\\'")
    db = get_database_instance()
    result = jsonify({"artist": db.execute_query_dict(
                        "SELECT artistName, COUNT(artistName) AS numberOfSongs FROM tracks "
                        "WHERE artistName = '" + artist_name + "' GROUP BY artistName;")[0],
                      "albums": db.execute_query_dict(
                        "SELECT albumName, COUNT(albumName) AS numberOfSongs, "
                        "albumArtist, albumCover, year, genre FROM tracks WHERE artistName = '" +
                        artist_name + "' GROUP BY artistName;"),
                      "songs": db.execute_query_dict(
                         "SELECT id, trackNumber, trackName, artistName, cdNumber, duration, year, genre, playCount,"
                         "CONCAT('"+library_config["public_path"]+"', SUBSTRING_INDEX(trackUrl,'"+library_config["library_path"]+"',-1)) as url "
                         "FROM tracks WHERE artistName = '" + artist_name +
                         "' ORDER BY (cdNumber * 1), (trackNumber * 1) ASC;")
                      })
    db.disconnect()
    return result
