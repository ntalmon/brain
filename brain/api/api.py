"""
| The api module contains all the entry points and API server invocation.
| All the entry, except api_get_snapshot_result_data, returns the result in JSON format.
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
    # Common way way to retrieve data from database and handle errors.
    # :param callback: callback to return results from database
    # :param to_json: should we json.dumps the results?
    # :return: the retrieved result, depending on to_json

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
def api_get_users():
    """
    Get the list of all supported users, including user id and username only.
    """

    logger.info('getting users')
    return common_api_wrapper(db_agent.find_users)


@app.route('/users/<int:user_id>')
def api_get_user(user_id: int):
    """
    Get the specified user's details: user id, username, birthday and gender.
    """

    logger.info(f'getting user: {user_id=}')
    return common_api_wrapper(lambda: db_agent.find_user(user_id))


@app.route('/users/<int:user_id>/snapshots')
def api_get_snapshots(user_id: int):
    """
    Get the list of the specified user's snapshots, including snapshot id and datetime only.
    """

    logger.info(f'getting user snapshots: {user_id=}')
    return common_api_wrapper(lambda: db_agent.find_snapshots(user_id))


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
def api_get_snapshot(user_id: int, snapshot_id: int):
    """
    Get the specified snapshot's details: snapshot id, datetime, and available results' names.
    """

    logger.info(f'getting user snapshot: {user_id=}, {snapshot_id=}')
    return common_api_wrapper(lambda: db_agent.find_snapshot(user_id, snapshot_id))


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>')
def api_get_snapshot_result(user_id: int, snapshot_id: int, result_name: str):
    """
    Get the specified snapshot's result in json format.
    """

    logger.info(f'getting snapshot results: {user_id=}, {snapshot_id=}, {result_name=}')
    return common_api_wrapper(lambda: db_agent.find_snapshot_result(user_id, snapshot_id, result_name))


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>/data')
def api_get_snapshot_result_data(user_id: int, snapshot_id: int, result_name: str):
    """
    Get the data of specified result name, when the result is big and contains file path to the full results.
    """

    # fetch the result itself, expect result to contain a file path, and return the file
    logger.info(f'getting result data: {user_id=}, {snapshot_id=}, {result_name=}')
    result = common_api_wrapper(lambda: db_agent.find_snapshot_result(user_id, snapshot_id, result_name), to_json=False)
    if 'path' not in result:
        logger.info(f'result {result_name} does not contain path, aborting with code=404')
        flask.abort(404)
    path = result['path']

    if not os.path.isfile(path):
        # file not found
        logger.warning(f'file not found for result {result_name}, {path=}, aborting with code=404')
        flask.abort(404)
    return flask.send_file(path, mimetype='image/jpeg', attachment_filename=f'{result_name}.jpg')


def init_db_agent(database_url):
    global db_agent
    db_agent = DBAgent(database_url)


def run_api_server(host, port, database_url):
    """
    Run the API server on the given host:port using the database at database_url.

    :param host: server hostname
    :param port: server port number
    :param database_url: address of the database to use
    """

    logger.info(f'running api server: {host=}, {port=}, {database_url=}')
    init_db_agent(database_url)
    logger.info('db is initialized, starting flask app')
    app.run(host, port)
