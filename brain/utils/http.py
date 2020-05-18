import requests


def get(url, expect=200):
    response = requests.get(url)
    if expect and response.status_code != expect:
        raise Exception(f'GET {url} failed with exit-code {response.status_code}')
    return response.text


def post(url, data, expect=200):
    response = requests.post(url, data)
    if expect and response.status_code != expect:
        raise Exception(f'POST {url} failed with exit-code {response.status_code}')
    return response.text
