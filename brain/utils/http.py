import requests


def get(url):
    response = requests.get(url)
    return response.text  # TODO: check response status


def post(url, data):
    response = requests.post(url, data)
    return response.status_code
