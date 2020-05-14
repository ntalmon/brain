from brain.utils.http import get


def api_get(host, port, path):
    url = f'http://{host}:{port}/{path}'
    result = get(url)
    return result
