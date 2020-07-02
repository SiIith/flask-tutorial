import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KET="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # overrides config from config.py in the instance folder
        app.config.from_pyfile('config.py', silent=True)
    else:
        # loads test config if it exists
        app.config.from_mapping(test_config)

    # try if the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page of hello world, with path "/hello"
    @app.route('/hello')
    def hello():
        return 'Hello world!'

    return app

