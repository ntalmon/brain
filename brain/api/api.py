import os

import flask
import flask_cors

from .db_agent import DBAgent
from ..utils.common import get_logger

logger = get_logger(__name__)
app = flask.Flask(__name__)
flask_cors.CORS(app)

db_agent = None  # type: DBAgent


def common_api_wrapper(callback, to_json=True):
    try:
        result = callback()
        if result is None:
            abort = 404
        else:
            return flask.jsonify(result) if to_json else result
    except Exception as error:
        logger.error(f'error while accessing database: {str(error)}')
        abort = 500
    logger.info(f'aborting with code={abort}')
    flask.abort(abort)


@app.route('/users')
def get_users():
    logger.info('getting users')
    return common_api_wrapper(db_agent.find_users)


@app.route('/users/<int:user_id>')
def get_user(user_id):
    logger.info(f'getting user: {user_id=}')
    return common_api_wrapper(lambda: db_agent.find_user(user_id))


@app.route('/users/<int:user_id>/snapshots')
def get_snapshots(user_id):
    logger.info(f'getting user snapshots: {user_id=}')
    return common_api_wrapper(lambda: db_agent.find_snapshots(user_id))


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
def get_snapshot(user_id, snapshot_id):
    logger.info(f'getting user snapshot: {user_id=}, {snapshot_id=}')
    return common_api_wrapper(lambda: db_agent.find_snapshot(user_id, snapshot_id))


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>')
def get_snapshot_result(user_id, snapshot_id, result_name):
    logger.info(f'getting snapshot results: {user_id=}, {snapshot_id=}, {result_name=}')
    return common_api_wrapper(lambda: db_agent.find_snapshot_result(user_id, snapshot_id, result_name))


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>/data')
def get_snapshot_result_data(user_id, snapshot_id, result_name):
    logger.info(f'getting result data: {user_id=}, {snapshot_id=}, {result_name=}')
    result = common_api_wrapper(lambda: db_agent.find_snapshot_result(user_id, snapshot_id, result_name), to_json=False)
    if 'path' not in result:
        logger.info(f'result {result_name} does not contain path, aborting with code=404')
        flask.abort(404)
    path = result['path']
    if not os.path.isfile(path):
        logger.warning(f'file not found for result {result_name}, {path=}, aborting with code=404')
        flask.abort(404)
    return flask.send_file(path, mimetype='image/jpeg', attachment_filename=f'{result_name}.jpg')


def init_db_agent(database_url):
    global db_agent
    db_agent = DBAgent(database_url)


def run_api_server(host, port, database_url):
    logger.info(f'running api server: {host=}, {port=}, {database_url=}')
    init_db_agent(database_url)
    logger.info('db is initialized, starting flask app')
    app.run(host, port)
