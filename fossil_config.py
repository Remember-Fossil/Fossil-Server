# -*- coding: utf-8 -*-
# Flask Options
DEBUG = True
SECRET_KEY = 'Development-key'


FACEBOOK = {}
if DEBUG:
    FACEBOOK['REDIRECT_URI'] = 'http://localhost:8080/login'
else:
    FACEBOOK['REDIRECT_URI'] = 'http://remember-fossil.appspot.com/login'

FACEBOOK['APP_ID'] = '407255472781563'
FACEBOOK['APP_SECRET'] = '45f3dc347e3721f0d4cf43e159d69c3c'
