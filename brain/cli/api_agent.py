from brain.utils.http import get


def api_get(host, port, path):
    # TODO: check status
    url = f'http://{host}:{port}/{path}'
    result = get(url)
    return result
