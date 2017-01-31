from flask import Blueprint, jsonify
from Database import get_database_instance
from YjmpdConfig import library_config

genreBlueprint = Blueprint('genreBlueprint', __name__)


@genreBlueprint.route('/')
def genres():
    db = get_database_instance()
    result = jsonify({"genres": db.execute_query_dict(
                        "SELECT genre, COUNT(genre) AS numberOfSongs FROM tracks GROUP BY genre;")
                      })
    db.disconnect()
    return result


@genreBlueprint.route('/<genre_name>')
def album(genre_name):
    genre_name = genre_name.replace('"', '\\"')
    genre_name = genre_name.replace("'", "\\'")
    db = get_database_instance()
    result = jsonify({"genre": db.execute_query_dict(
                        "SELECT genre, COUNT(genre) AS numberOfSongs FROM tracks "
                        "WHERE genre = '" + genre_name + "' GROUP BY genre;")[0],
                      "albums": db.execute_query_dict(
                        "SELECT albumName, COUNT(albumName) AS numberOfSongs, "
                        "albumArtist, albumCover, year, genre FROM tracks WHERE genre = '" +
                        genre_name + "' GROUP BY albumName;"),
                      "songs": db.execute_query_dict(
                         "SELECT id, trackNumber, trackName, artistName, cdNumber, duration, year, genre, playCount,"
                         "CONCAT('"+library_config["public_path"]+"', SUBSTRING_INDEX(trackUrl,'"+library_config["library_path"]+"',-1)) as url "
                         "FROM tracks WHERE genre = '" + genre_name +
                         "' ORDER BY (cdNumber * 1), (trackNumber * 1) ASC;")
                      })
    db.disconnect()
    return result
