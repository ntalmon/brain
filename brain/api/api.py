import os

import flask
import flask_cors
from brain.api.db_agent import DBAgent

app = flask.Flask(__name__)
flask_cors.CORS(app)

db_agent = None


@app.route('/users')
def get_users():
    res = db_agent.find_users()
    return flask.jsonify(res)


@app.route('/users/<int:user_id>')
def get_user(user_id):
    res = db_agent.find_user(user_id)
    return flask.jsonify(res)


@app.route('/users/<int:user_id>/snapshots')
def get_snapshots(user_id):
    res = db_agent.find_snapshots(user_id)
    return flask.jsonify(res)


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
def get_snapshot(user_id, snapshot_id):
    res = db_agent.find_snapshot(user_id, snapshot_id)
    return flask.jsonify(res)


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>')
def get_snapshot_result(user_id, snapshot_id, result_name):
    res = db_agent.find_snapshot_result(user_id, snapshot_id, result_name)
    return flask.jsonify(res)


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>/data')
def get_snapshot_result_data(user_id, snapshot_id, result_name):
    # TODO: handle case where result is text only
    res = db_agent.find_snapshot_result(user_id, snapshot_id, result_name)
    file_path = res['path']  # TODO: check file indeed exists
    if not os.path.isfile(file_path):
        flask.abort(404)
    return flask.send_file(file_path, mimetype='image/jpeg', attachment_filename=f'{result_name}.jpg')


def init_db_agent(database_url):
    global db_agent
    db_agent = DBAgent(database_url)


def run_api_server(host, port, database_url):
    init_db_agent(database_url)
    app.run(host, port)
