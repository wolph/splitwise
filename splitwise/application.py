import flask_failsafe


@flask_failsafe.failsafe
def get_app():
    import flask
    from flask.ext import compress

    # Create the app
    app = flask.Flask(
        __name__.split('.')[0],
        static_folder='../static',
        template_folder='../templates',
    )

    # Load the configs
    app.config.from_object('splitwise.default_settings')
    app.config.from_pyfile('../settings.py', silent=True)
    app.config.from_envvar('SPLITWISE_SETTINGS', silent=True)

    # Enable javascript/css compression
    compress.Compress(app)

    return app

