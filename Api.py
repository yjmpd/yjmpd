#!/usr/bin/env python3
from flask import Flask
from flask_cors import CORS

from YjmpdConfig import http_config
from blueprints.AlbumBlueprint import albumBlueprint
from blueprints.ArtistBlueprint import artistBlueprint
from blueprints.GenreBlueprint import genreBlueprint
from blueprints.SongBlueprint import songBlueprint
from blueprints.YearBlueprint import yearBlueprint


class Api:
    app = Flask("YJMPD API")
    CORS(app)

    def __init__(self):
        self.app.register_blueprint(albumBlueprint, url_prefix='/albums')
        self.app.register_blueprint(songBlueprint, url_prefix='/songs')
        self.app.register_blueprint(genreBlueprint, url_prefix='/genres')
        self.app.register_blueprint(artistBlueprint, url_prefix='/artists')
        self.app.register_blueprint(yearBlueprint, url_prefix='/years')

        if http_config["ssl"]:
            context = (http_config["certificate"], http_config["privatekey"])
            self.app.run(host=http_config["address"], port=http_config["port"], debug=False, threaded=True, ssl_context=context)
        else:
            self.app.run(host=http_config["address"], port=http_config["port"], debug=False, threaded=True)

