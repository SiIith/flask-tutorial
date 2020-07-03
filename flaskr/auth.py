"""
authentication blueprint. Related views and code are registered here first before passing to application when
available in factory function
"""

import functools # module for higher order functions (i.e. funcs that act on or returns other funcs)

from flask import Blueprint, flash, g, redirect, render_template, request, sessions, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db


# creates a blueprint named auth and prepend "/auth" to all URLs associated with this blueprint
# __name__ passes the current location of where the blueprint is defined to the bp
# this bp is exported to __init__ and registered
bp = Blueprint('auth', __name__, url_prefix='/auth')


# associates the url with the function register. The complete url is therefore '.../auth/register'
# 
@bp.route('/register', method = ('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = "Require a username"
        elif not password:
            error = "Require a password"
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
            error = "User {} already exists.".format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?,?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')



