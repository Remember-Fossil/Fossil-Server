# -*- coding: utf-8 -*-
from flask import current_app, Blueprint, request, render_template
from flask import session, url_for, redirect
from fb import FB, Graph
from .models import User, FacebookSession
from .utils import check_facebook_session

blue_auth = Blueprint('auth', __name__, url_prefix='')

@blue_auth.route('/')
@blue_auth.route('/login')
def login():
    if not 'user_id' in session:
        if request.args.get('code', False):
            fb = FB(current_app.config['FACEBOOK']['APP_ID'],
                    current_app.config['FACEBOOK']['APP_SECRET'])
            access_token, expires = fb.get_access_token(request.args['code'])
            graph = Graph(access_token)

            profile_data = graph.feed_get('me', {})
            user = User.all().filter('facebook_id =', profile_data['id']).get()
            if  user == None:
                user = User()
                user.facebook_id = profile_data['id']
                user.name = "{0}{1}".format(
                    profile_data['last_name'].encode('utf-8'),
                    profile_data['first_name'].encode('utf-8'))
                image_url = graph.feed_get('me/picture',
                                           {'redirect':False})['data']['url']
                user.profile_image = ''
                user.put()

            fb_session = FacebookSession.all().filter('user =', user.key()).get()
            if check_facebook_session(fb_session):
                fb_session.access_token = access_token
                fb_session.expires = int(expires)
                fb_sessoin.put()
            else:
                fb_session = FacebookSession()
                fb_session.user = user
                fb_session.token = access_token
                fb_session.expires = int(expires)
                fb_session.put()

            session['user_id'] = user.key().id_or_name()
        else:
            return render_template('login.html', facebook=current_app.config['FACEBOOK'])
    return render_template('group_list.html')


@blue_auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

