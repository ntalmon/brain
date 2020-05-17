import os

import flask

from brain import app_path

api_url = ''
build_path = app_path / 'build'
app = flask.Flask(__name__, static_folder=str(build_path), template_folder=str(build_path))


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != '' and os.path.exists(os.path.join(app.static_folder, path)):
        return flask.send_from_directory(app.static_folder, path)
    return flask.render_template('index.html', api_url=api_url)


def shutdown_server():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()


def run_server(host, port, api_host, api_port):
    global api_url
    api_url = f'http://{api_host}:{api_port}'
    app.run(host=host, port=port, threaded=True)
