# -*- coding: utf-8 -*-

from flask import g, session, redirect, url_for
from .models import User, FacebookSession
import functools

# custom_function을 채우면 작동한다
# 아마 안채워도 되는게있긴할텐데.t.
# blueprint와 꼬임을 방지하기위해 wraps를 쓰는것 같기도...
class LoginRequired(object):
    def __init__(self, *args, **kwargs):
        self.custom_function = kwargs.get('custom_function', 'auth.login')

    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            if not session.get('user_id', False):
                return redirect(url_for(self.custom_function))
            user = User.get_by_id(session['user_id'])
            g.user = user
            g.fb_session = FacebookSession.all().filter('user = ', user).get()

            return fn(*args, **kwargs)
        return decorated

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id', False):
            return redirect(url_for('auth.login'))
        user = User.get_by_id(session['user_id'])
        g.user = user
        g.fb_session = FacebookSession.all().filter('user = ', user).get()
        return f(*args, **kwargs)
    return decorated_function
