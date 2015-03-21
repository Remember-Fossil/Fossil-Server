# -*- coding: utf-8 -*-
from flask import Flask


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from fossil.views.views import blue_home

    app.register_blueprint(blue_home)

    return app

