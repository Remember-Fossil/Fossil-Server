# -*- coding: utf-8 -*-
from google.appengine.ext import db


# class User(db.Model):
#    email = db.StringProperty()
#    password = db.StringProperty()
#    name = db.StringProperty()

#    peach = db.IntegerProperty(default=0)

#    signup_datetime = db.DateTimeProperty(auto_now_add=True)

#    friends = db.ListProperty(db.Key)

class User(db.Model):
    facebook_id = db.StringProperty(unique=True)
    name = db.StringProperty()
    profile_image = db.StrginProperty()
    created_at  = db.DateTimeProperty(auto_now_add=True)

class FacebookSession(db.Model):
    user = db.ReferenceProperty(User)
    token = db.StringProperty()
    expire = db.IntegerProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
