import flask

app = flask.Flask(__name__)


@app.route('/users')
def get_users():
    pass


def run_api_server(host, port, database_url):  # TODO: handle database_url
    app.run(host, port)
