import flask

app = flask.Flask(__name__)


@app.route('/users')
def get_users():
    pass


@app.route('/users/<int:user-id>')
def get_user(user_id):
    pass


@app.route('/users/<int:user-id>/snapshots')
def get_snapshots(user_id):
    pass


@app.route('/users/<int:user-id>/snapshots/<int:snapshot-id>')
def get_snapshot(user_id, snapshot_id):
    pass


@app.route('/users/<int:user-id>/snapshots/<int:snapshot-id>/<result-name>')
def get_snapshot_result(user_id, snapshot_id, result_name):
    pass


@app.route('/users/<int:user-id>/snapshots/<int:snapshot-id>/<result-name>/data')
def get_snapshot_result_data(user_id, snapshot_id, result_name):
    pass


def run_api_server(host, port, database_url):  # TODO: handle database_url
    app.database_url = database_url
    app.run(host, port)
