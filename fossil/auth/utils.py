# -*- coding: utf-8 -*-
from .models import FacebookSession
from datetime import datetime, timedelta

def check_facebook_session(fb_session):
    if fb_session == None:
        return False

    today = datetime.today()
    if today > fb_session.created_at+timedelta(milliseconds = fb_session.expires):
        return True;

    else:
        return False;
