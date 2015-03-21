# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, g, request, redirect, url_for
from .models import Group, Member
from fossil.fb import Graph
from fossil.auth.decorators import login_required

blue_groups = Blueprint('groups', __name__, url_prefix='/groups')


@blue_groups.route('/')
@login_required
def group_list():
    groups = Group.get_groups_by_user(g.user)
    return render_template('group_list.html', groups = groups)


@blue_groups.route('/add', methods=['GET', 'POST'])
@login_required
def group_add():
    graph = Graph(g.fb_session.token)
    if request.method == 'GET':
        id_list = []
        for group in Group.get_groups_by_user(g.user):
            id_list.append(group.group_id)

        groups = graph.get_groups()
        filter(lambda x: x['id'] in id_list, groups)

        return render_template('group_add.html', groups = groups)
    elif request.method == 'POST':
        group_id = request.form.get('group_id', False)
        if not group_id:
            return abort(404)

        group_info = graph.get('/{0}'.format(group_id), {})
        group = Group()
        group.name = group_info['name']
        group.cover_image = 'http://cfile2.uf.tistory.com/image/1763F50C4BBD32EF052575'
        group.group_id = group_info['id']
        group.put()

        group_members = graph.get('/{0}/members'.format(group_id), {})

        #실제로 절대하면안되는짓임 100% timeout
        for user in group_members['data']:
            user_info = graph.get('/{0}'.format(user['id']), {})
            member = Member()
            member.group = group
            member.name = user_info['name']
            image_url = graph.get('/me/picture', {'redirect': False})['data']['url']
            member.profile_image = image_url
            member.facebook_id = user_info['id']
            member.put()

        return redirect(url_for('groups.group_list'))
    else:
        abort(403)


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
