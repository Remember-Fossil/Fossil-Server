# -*- coding: utf-8 -*-
from .utils import urldecode
import requests
from flask import current_app

class FB:
    def __init__(self, fb_app_id, fb_app_secret):
        self._fb_app_id = fb_app_id
        self._fb_app_secret = fb_app_secret

    def get_access_token(self, code):
        url = 'https://graph.facebook.com/oauth/access_token'
        response = requests.get(url, params = {
            'client_id': self._fb_app_id,
            'client_secret': self._fb_app_secret,
            'redirect_uri': current_app.config['FACEBOOK_REDIRECT_URL'],
            'code': code
        })

        if 'error' in response.content:
            raise ValueError

        data = urldecode(response.content)
        return data['access_token']

