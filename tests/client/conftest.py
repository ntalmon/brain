import json


class MockReader:
    def __init__(self, path):
        with open('../resources/tests_sample.mind.json', 'r') as file:
            data = json.load(file)
        self.user = data[0]
        self.snapshots = data[1:]
