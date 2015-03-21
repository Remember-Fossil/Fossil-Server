# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, g
from .models import Group, Member, GameLog
from fossil.auth.decorators import login_required
import random
import json


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


@blue_groups.route('/<int:group_id>/exam/get_question')
@login_required
def group_exam_get_question(group_id):
    group = Group.get_by_id_with_user(group_id, g.user)
    if not group:
        abort(404)

    last_game = GameLog.all() \
        .filter('group =', group.key()) \
        .filter('user =', g.user.key()) \
        .filter('status =', GameLog.NOT_SOLVED) \
        .get()

    if last_game:
        game = last_game
    else:
        members = group.member_set
        if members is None or len(members) == 0:
            return 'No members!!'

        while True:
            question_member = random.choice(members).get()
            if question_member.facebook_id == user.facebook_id:
                continue
            break

        answer_members = []
        for i in range(4):
            while True:
                member = random.choice(members).get()
                if member.facebook_id == user.facebook_id:
                    continue
                if member.facebook_id == question_member.facebook_id:
                    continue
                break
            answer_members.append(member)

        if random.randint(1, 5) != 1:
            # Case: Answer exist
            answer_num = random.randint(0, 3)
            answer_members[answer_num] = question_member

        answers = [
            answer_member.facebook_id for answer_member in answer_members]
        game = GameLog(group=group,
                       user=g.user,
                       question_member=question_member,
                       answers=json.dumps(answers),
                       status=GameLog.NOT_SOLVED)
        game.put()

    return jsonify({'game_id': game.key().id_or_name(),
                    'question_image': game.question_member.profile_image,
                    'answers': answers})


@blue_groups.route('/<int:group_id>/exam/<int:game_id>/check',
                   methods=['POST'])
@login_required
def group_exam_check(group_id, game_id):
    group = Group.get_by_id_with_user(group_id, g.user)
    if not group:
        abort(404)

    game = GameLog.get_by_id(game_id)
    if not game or game.user.key() != g.user.key() or \
            game.group.key() != group.key() or \
            game.status != GameLog.NOT_SOLVED:
        abort(404)

    selected = request.form['selected']  # 0(Not exists) 1 2 3 4
    answers = json.loads(game.answers)

    if question_member.facebook_id in answers:
        # If answer is exist
        if answers[selected] == question_member.facebook_id:
            # Correct!
            game.user_answer = question_member
            game.status = GameLog.CORRECT
            game.put()
            return jsonify({'result': 'correct'})
        else:
            # Incorrect!
            user_select_member = Member.all() \
                .filter('group =', group.key()) \
                .filter('facebook_id =', answers[selected]) \
                .get()
            game.user_answer = user_select_member
            game.status = GameLog.INCORRECT
            game.put()
            # TODO: Post article on group.
            return jsonify({'result': 'incorrect',
                            'answer_name': question_member.name})
    else:
        # If answer is NOT EXIST
        if selected == 0:
            # Correct!
            game.status = GameLog.CORRECT
            game.put()
            return jsonify({'result': 'correct'})
        else:
            # Incorrect!
            game.status = GameLog.INCORRECT
            game.put()
            # TODO: Post article on group.
            return jsonify({'result': 'incorrect',
                            'answer_name': question_member.name})
