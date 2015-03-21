# -*- coding: utf-8 -*-

from flask import g, session, redirect, url_for
from functools import wraps
from .models import User, FacebookSession


# class LoginRequired(object):
# uf_function으로 url_for 호출함수 커스텀가능
#     def __init__(self, uf_function='auth.login'):
#         self.uf_function = uf_function

#     def __call__(self, func):
#         @wraps(func)
#         def wrapper_func(*args, **kwargs):
#             if not session.get('user_id', False):
#                 return redirect(url_for(self.uf_function))
#             g.user = User.get_by_id(session['user_id'])
#             return func(*args, **kwargs)
#         return wrapper_func

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id', False):
            return redirect(url_for('auth.login'))
        user = User.get_by_id(session['user_id'])
        g.user = user
        g.fb_session = FacebookSession.all().filter('user = ', user).get()
        return f(*args, **kwargs)
    return decorated_function
