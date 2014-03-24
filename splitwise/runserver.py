import flask_failsafe


@flask_failsafe.failsafe
def get_app():
    from splitwise import app
    return app


def run():
    app = get_app()
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['SERVER_HOST'],
        port=app.config['SERVER_PORT'],
    )

if __name__ == '__main__':
    run()

