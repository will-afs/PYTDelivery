import os, json

from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__) #, instance_relative_config=True
    try:
        launch_mode = os.environ['FLASK_ENV']
    except KeyError:
        launch_mode = None
    possible_launch_mode_values = ('prod', 'dev', 'test')
    if launch_mode not in possible_launch_mode_values:
        raise ValueError("Expected value in '{}' for FLASK_ENV environment variable. Got '{}' instead.".format(possible_launch_mode_values[:], launch_mode))
    elif launch_mode == 'prod':
        app.config.from_object("config.ProdConfig")
    elif launch_mode == 'dev':
        app.config.from_object("config.DevConfig")
    elif launch_mode == 'test':
        app.config.from_object("config.TestConfig")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from flaskapp.db import db
    db.init_app(app) # Fake friend : just to register the database commands into the app

    # apply the blueprints to the app
    from flaskapp import views
    app.register_blueprint(views.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    # app.add_url_rule("/", endpoint="index")

    return app
