import requests


def post(url, data):
    response = requests.post(url, data)
    return response.status_code
