from flask import current_app, abort, request

from . import main


@main.route('/shutdown')
def shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'shutting down...'


@main.route('/')
def index():
    return '<h1>hello flask!</h1>'
