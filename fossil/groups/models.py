# -*- coding: utf-8 -*-
from google.appengine.ext import db
from fossil.auth.models import User


class Group(db.Model):
    name = db.StringProperty()
    cover_image = db.StringProperty()
    group_id = db.StringProperty()
    owner = db.ReferenceProperty(User)

    @classmethod
    def get_by_id_with_user(cls, group_id, user):
        group = cls.get_by_id(group_id)

        if group is None:
            return None

        member = Member.all() \
            .filter('group =', group.key()) \
            .filter('facebook_id =', user.facebook_id) \
            .get()

        if member:
            return group

        return None


class Member(db.Model):
    group = db.ReferenceProperty(Group)

    name = db.StringProperty()
    profile_image = db.StringProperty()
    facebook_id = db.StringProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
