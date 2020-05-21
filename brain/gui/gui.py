import os

import flask

from brain import app_path

api_url = ''
build_path = app_path / 'build'
app = flask.Flask(__name__, static_folder=str(build_path), template_folder=str(build_path))


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    try:
        if path != '' and os.path.exists(os.path.join(app.static_folder, path)):
            return flask.send_from_directory(app.static_folder, path)
        return flask.render_template('index.html', api_url=api_url)
    except Exception as error:
        print(f'Exception: {str(error)}')
        flask.abort(500)


def run_server(host, port, api_host, api_port):
    global api_url
    api_url = f'http://{api_host}:{api_port}'
    app.run(host=host, port=port, threaded=True)
