# -*- coding: utf-8 -*-

from flask import g, session, redirect, url_for
from .models import User

class LoginRequired(object):

    def __init__(self, *args, **kwargs):
        super(LoginRequired, self).__init__(*args, **kwargs)

        uf_function = kwargs.pop('uf_fucntion', False)
        if uf_function:
            self.uf_function = uf_function
        else:
            self.uf_function = 'auth.login'

    def __call__(self, func):
        def wrapper_func(*args):
            if not session.get('user_id', False):
                return redirect(url_for(self.uf_function))
            g.user = User.get_by_id(session['user_id'])
            return func(*args)

        return wrapper_func

