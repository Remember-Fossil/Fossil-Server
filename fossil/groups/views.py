# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort
from .models import Group, Member

blue_groups = Blueprint('groups', __name__, url_prefix='/groups')


@blue_groups.route('/')
def group_list():
    return render_template('group_list.html')


@blue_groups.route('/<int:group_id>')
@blue_groups.route('/<int:group_id>/members')
def group_members(group_id):
    group = Group.get_by_id_with_user(group_id, user)
    if not group:
        abort(404)

    return render_template('group_members.html', group=group)


@blue_groups.route('/<int:group_id>/exam')
def group_exam(group_id):
    group = Group.get_by_id_with_user(group_id, user)
    if not group:
        abort(404)

    return render_template('/group_exam.html', group=group)
