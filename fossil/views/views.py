# -*- coding: utf-8 -*-
from flask import current_app, Blueprint, request, render_template, session
from fb import FB, Graph
blue_home = Blueprint('main', __name__, url_prefix='')

@blue_home.route('/login', methods=['GET'])
def login():
    if not 'user_id' in session:
        if request.args.get('code', False):
            fb = FB(current_app.config['FACEBOOK_APP_ID'], current_app.config['FACEBOOK_APP_SECRET'])
            access_token = fb.get_access_token(request.form['code'])
            graph = Graph(access_token)

            profile_data = graph.feed_get('/me', {})
            print profile_data
        else:
            pass

    return render_template('home.html', profile_data=profile_data)
