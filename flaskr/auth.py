"""
authentication blueprint. Related views and code are registered here first before passing to application when
available in factory function
A view is a function that responds to requests to the application.
The name associated with a view is called the endpoint, which is by default the name of the view function
"""

import functools  # module for higher order functions (i.e. funcs that act on or returns other funcs)

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db


# creates a blueprint named auth and prepend "/auth" to all URLs associated with this blueprint
# __name__ passes the current location of where the blueprint is defined to the bp
# this bp is exported to __init__ and registered
bp = Blueprint('auth', __name__, url_prefix='/auth')


# associates the url with the function register.
# the endpoint/name of the view is by default the same to the view function
# in this blueprint, every view is prepended with the name of the bp
# The complete url is therefore '.../auth/register'
@bp.route('/register', methods = ('GET', 'POST'))
def register():
    # if a form is submitted (i.e. method 'POST'), reads the information and starts validating
    # form is a special dict-like object that maps key-val pairs
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = "Require a username"
        elif not password:
            error = "Require a password"

        # fetchone returns one row of the query and asserts it's not null
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = "User {} already exists.".format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?,?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            # redirects to login page if no error is caught
            return redirect(url_for('auth.login'))

        # flashes error message is error is caught
        flash(error)

    return render_template('auth/register.html')


# the login url similar to register
@bp.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        # stores user id in a new session, which is a dict-like object that stores data across requests.
        # the data is stored in a cookie sent to the browser and then sent back to Flask to be signed in
        # subsequent requests
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# registers a function that runs before the view function
# checks if a user is stored and pass it to g.user which will be stored for the request duration
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# logout functionality
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# a decorator that checks if the user is logged in and redirects to login page if not so.
# if logged in the current view is continued normally
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view

