"""
This module contains all the API entry points, and invoking the API server.
"""
import os

import flask
import flask_cors

from brain.utils.common import get_logger
from .db_agent import DBAgent

logger = get_logger(__name__)
app = flask.Flask(__name__)
flask_cors.CORS(app)

db_agent = None  # type: DBAgent


def common_api_wrapper(callback, to_json=True):
    """
    Common way way to retrieve data from database and handle errors.
    :param callback: callback to return results from database
    :param to_json: should we json.dumps the results?
    :return: the retrieved result, depending on to_json
    """
    try:
        result = callback()
        # None result is returned when we could not find any match in database.
        if result is None:
            abort = 404
        else:
            # return result in format depending on to_json
            return flask.jsonify(result) if to_json else result
    except Exception as error:
        logger.error(f'error while accessing database: {str(error)}')
        abort = 500  # server error
    logger.info(f'aborting with code={abort}')
    flask.abort(abort)


@app.route('/users')
def get_users():
    """
    API entry point for getting all the users.
    :return: list of users, each one contains user id and username.
    """
    logger.info('getting users')
    return common_api_wrapper(db_agent.find_users)


@app.route('/users/<int:user_id>')
def get_user(user_id):
    """
    API entry point for getting a user by user id

    :return: the user id, username, birthday, and gender of the user.
    """
    logger.info(f'getting user: {user_id=}')
    return common_api_wrapper(lambda: db_agent.find_user(user_id))


@app.route('/users/<int:user_id>/snapshots')
def get_snapshots(user_id):
    """
    API entry point to get all snapshots of a user by user id.

    :return: a list of snapshots, each one contains snapshot uuid and datetime.
    """
    logger.info(f'getting user snapshots: {user_id=}')
    return common_api_wrapper(lambda: db_agent.find_snapshots(user_id))


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
def get_snapshot(user_id, snapshot_id):
    """
    API entry point for getting a snapshot of a user by user id and snapshot id.

    :return: the uuid, datetime, and list of available results names of the snapshot.
    """
    logger.info(f'getting user snapshot: {user_id=}, {snapshot_id=}')
    return common_api_wrapper(lambda: db_agent.find_snapshot(user_id, snapshot_id))


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>')
def get_snapshot_result(user_id, snapshot_id, result_name):
    """
    API entry point for getting a result of a snapshot, by user id, snapshot id, and result name.

    :return: the result, as returned from database.
    """
    logger.info(f'getting snapshot results: {user_id=}, {snapshot_id=}, {result_name=}')
    return common_api_wrapper(lambda: db_agent.find_snapshot_result(user_id, snapshot_id, result_name))


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>/data')
def get_snapshot_result_data(user_id, snapshot_id, result_name):
    """
    API entry for getting the data of result, when the result contains a path to some file.

    :return: the file data.
    """
    logger.info(f'getting result data: {user_id=}, {snapshot_id=}, {result_name=}')
    # at first, get the textual result from database
    result = common_api_wrapper(lambda: db_agent.find_snapshot_result(user_id, snapshot_id, result_name), to_json=False)
    # expecting result to include path, otherwise /data is invalid for this result
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
    """
    Run the API server on the given host:port using the database at database_url.
    """
    logger.info(f'running api server: {host=}, {port=}, {database_url=}')
    init_db_agent(database_url)
    logger.info('db is initialized, starting flask app')
    app.run(host, port)
