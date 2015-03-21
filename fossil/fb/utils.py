# -*- coding: utf-8 -*-

def urldecode(res):
    return dict([data.split('=') for data in res.split('&') if True])

