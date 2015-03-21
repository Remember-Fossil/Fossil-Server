# -*- coding: utf-8 -*-
# Flask Options
DEBUG = False
SECRET_KEY = 'Development-key'


if DEBUG:
    FACEBOOK_REDIRECT_URL = 'http://localhost:8080'
else:
    FACEBOOK_REDIRECT_URL = 'remember-fossil.appspot.com'

FACEBOOK_APP_ID = '407255472781563'
FACEBOOK_APP_SECRET = '45f3dc347e3721f0d4cf43e159d69c3c'
