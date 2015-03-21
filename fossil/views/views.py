# -*- coding: utf-8 -*-
from flask import current_app, Blueprint, request, render_template

blue_home = Blueprint('test', __name__, url_prefix='')


@blue_home.route('/')
def home():
    return render_template('home.html')

