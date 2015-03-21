# -*- coding: utf-8 -*-
from flask import Flask


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from fossil.auth.views import blue_auth
    from fossil.groups.views import blue_groups

    app.register_blueprint(blue_auth)
    app.register_blueprint(blue_groups)

    return app

