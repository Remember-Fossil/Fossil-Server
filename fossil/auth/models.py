# -*- coding: utf-8 -*-
from google.appengine.ext import db


class User(db.Model):
    facebook_id = db.StringProperty()
    name = db.StringProperty()
    profile_image = db.StringProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)


class FacebookSession(db.Model):
    user = db.ReferenceProperty(User)
    token = db.StringProperty()
    expires = db.IntegerProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
