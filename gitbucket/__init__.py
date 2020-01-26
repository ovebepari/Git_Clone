import os

from flask import Flask, g, url_for, render_template, redirect

from . import auth, dashboard


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth, dashboard, repository, global_profile
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.dashbp)
    app.register_blueprint(repository.repo_bp)
    app.register_blueprint(global_profile.global_profileBP)


    # Redirecting every requests to datshboard.index
    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))

    return app