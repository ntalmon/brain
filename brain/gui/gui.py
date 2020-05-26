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
def serve(path):
    logger.info(f'serving {path=}')
    try:
        if path != '' and os.path.exists(os.path.join(app.static_folder, path)):
            return flask.send_from_directory(app.static_folder, path)
        return flask.render_template('index.html', api_url=api_url)
    except Exception as error:
        logger.error(f'error while server route: {str(error)}, aborting 500')
        flask.abort(500)


def run_server(host, port, api_host, api_port):
    global api_url
    api_url = f'http://{api_host}:{api_port}'
    logger.info(f'starting flask app on {host}:{port}')
    app.run(host=host, port=port, threaded=True)
