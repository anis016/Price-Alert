'''
__author__ = 'anis016'
Date: 01.09.16
Time: 03:23
'''
from functools import wraps

from flask import request
from flask import session
from flask import url_for
from werkzeug.utils import redirect

from src.app import app


def requires_login(function):

    @wraps(function)
    def wrapper_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))  # once login then goto the place where user was present
        return function(*args, **kwargs)

    return wrapper_function


def requires_admin_permission(function):

    @wraps(function)
    def wrapper_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in app.config['ADMINS']:
            return redirect(url_for('users.login_user'))
        return function(*args, **kwargs)
    return wrapper_function
