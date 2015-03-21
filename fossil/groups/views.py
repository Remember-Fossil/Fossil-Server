# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, g
from .models import Group, Member
from fossil.auth.decorators import login_required
blue_groups = Blueprint('groups', __name__, url_prefix='/groups')


@blue_groups.route('/')
@login_required
def group_list():
    return render_template('group_list.html')


@blue_groups.route('/add')
@login_required
def group_add():
    return render_template('group_add.html')


@blue_groups.route('/<int:group_id>')
@blue_groups.route('/<int:group_id>/members')
@login_required
def group_members(group_id):
    group = Group.get_by_id_with_user(group_id, g.user)
    if not group:
        abort(404)

    return render_template('group_members.html', group=group)


@blue_groups.route('/<int:group_id>/exam')
@login_required
def group_exam(group_id):
    group = Group.get_by_id_with_user(group_id, g.user)
    if not group:
        abort(404)

    return render_template('/group_exam.html', group=group)
