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

    # imports init_app from same package
    from . import db
    db.init_app(app)

    # imports auth and register the blueprint "bp" to the app
    from . import auth
    app.register_blueprint(auth.bp)

    # there's no prefix for blog but indices, since blog is the main feature of flaskr and it makes sense
    # to have blog as the main index, with blog.index being the endpoint of the index view.
    # It also makes sense, if blog is one of the features, to give blog bp a url prefix and defines a
    # separate index view in the factory.
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
