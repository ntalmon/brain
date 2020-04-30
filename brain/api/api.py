import flask
import flask_cors
from brain.api.db_agent import MongoDBAgent

app = flask.Flask(__name__)
flask_cors.CORS(app)


@app.route('/users')
def get_users():
    res = app.agent.find_users()
    return flask.jsonify(res)


@app.route('/users/<int:user_id>')
def get_user(user_id):
    return app.agent.find_user(user_id)


@app.route('/users/<int:user_id>/snapshots')
def get_snapshots(user_id):
    return app.agent.find_snapshots(user_id)


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
def get_snapshot(user_id, snapshot_id):
    return app.agent.find_snapshot(user_id, snapshot_id)


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>')
def get_snapshot_result(user_id, snapshot_id, result_name):
    return app.agent.find_snapshot_result(user_id, snapshot_id, result_name)


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>/data')
def get_snapshot_result_data(user_id, snapshot_id, result_name):
    pass  # TODO: find a way to return the data


def run_api_server(host, port, database_url):
    app.database_url = database_url
    app.agent = MongoDBAgent(database_url)
    app.run(host, port)
