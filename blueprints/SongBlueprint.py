from flask import Blueprint, jsonify
from Database import get_database_instance
from YjmpdConfig import library_config

songBlueprint = Blueprint('songBlueprint', __name__)


@songBlueprint.route('/')
def songs():
    db = get_database_instance()
    result = jsonify({"songs": db.execute_query_dict(
                        "SELECT id, trackNumber, trackName, artistName, cdNumber, duration, year, genre, playCount,"
                        "albumName, albumArtist, albumCover, "
                        "CONCAT('"+library_config["public_path"]+"', SUBSTRING_INDEX(trackUrl,'"+library_config["library_path"]+"',-1)) as url "
                        "FROM tracks ORDER BY albumName, (cdNumber * 1), (trackNumber * 1) ASC;")
                      })
    db.disconnect()
    return result
