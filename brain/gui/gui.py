"""
The GUI module contains a flask app that which is the web application backend.
"""

import os

import flask

from brain import app_path
from brain.utils.common import get_logger

logger = get_logger(__name__)
api_url = ''
build_path = app_path / 'build'
app = flask.Flask(__name__, static_folder=str(build_path), template_folder=str(build_path))


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path: str):
    """
    Main entry point for the app backend.
    Serves both different routes in the app, and resources ion the app.

    :param path: the relative path of the current request
    """

    logger.info(f'serving {path=}')
    try:
        if path != '' and os.path.exists(os.path.join(app.static_folder, path)):
            # serve resource
            return flask.send_from_directory(app.static_folder, path)
        # serve route, which is, rending the index.html
        return flask.render_template('index.html', api_url=api_url)
    except Exception as error:
        logger.error(f'error while server route: {str(error)}, aborting 500')
        flask.abort(500)


def run_server(host: str, port: int, api_host: str, api_port: int):
    """
    Runs the GUI server.

    :param host: GUI server hostname.
    :param port: GUI server port number.
    :param api_host: API server hostname for the app to use.
    :param api_port: API server port number for the app to use.
    """

    global api_url
    api_url = f'http://{api_host}:{api_port}'
    logger.info(f'starting flask app on {host}:{port}')
    app.run(host=host, port=port, threaded=True)
