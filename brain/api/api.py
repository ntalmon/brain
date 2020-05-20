import os
import pathlib

import flask
import flask_cors

from .db_agent import DBAgent

app = flask.Flask(__name__)
flask_cors.CORS(app)

db_agent = None  # type: DBAgent


def common_api_wrapper(callback, to_json=True):
    try:
        result = callback()
        if result is None:
            flask.abort(404)
        return flask.jsonify(result) if to_json else result
    except Exception as error:
        print(str(error))
        flask.abort(500)


@app.route('/users')
def get_users():
    return common_api_wrapper(db_agent.find_users)


@app.route('/users/<int:user_id>')
def get_user(user_id):
    return common_api_wrapper(lambda: db_agent.find_user(user_id))


@app.route('/users/<int:user_id>/snapshots')
def get_snapshots(user_id):
    return common_api_wrapper(lambda: db_agent.find_snapshots(user_id))


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
def get_snapshot(user_id, snapshot_id):
    return common_api_wrapper(lambda: db_agent.find_snapshot(user_id, snapshot_id))


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>')
def get_snapshot_result(user_id, snapshot_id, result_name):
    return common_api_wrapper(lambda: db_agent.find_snapshot_result(user_id, snapshot_id, result_name))


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>/data')
def get_snapshot_result_data(user_id, snapshot_id, result_name):
    result = common_api_wrapper(lambda: db_agent.find_snapshot_result(user_id, snapshot_id, result_name), to_json=False)
    if 'file_name' not in result:
        flask.abort(404)
    file_name = result['file_name']
    snapshot = common_api_wrapper(lambda: db_agent.find_snapshot(user_id, snapshot_id, include_path=True),
                                  to_json=False)
    path = snapshot['path']
    file_path = str(pathlib.Path(path) / file_name)
    if not os.path.isfile(file_path):
        flask.abort(404)
    return flask.send_file(file_path, mimetype='image/jpeg', attachment_filename=f'{result_name}.jpg')


def init_db_agent(database_url):
    global db_agent
    db_agent = DBAgent(database_url)


def run_api_server(host, port, database_url):
    init_db_agent(database_url)
    app.run(host, port)
