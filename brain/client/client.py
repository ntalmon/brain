from brain.client.reader import MindReader


def upload_sample(host, port, path):
    """
    TODO: add connection to server and upload sample
    """
    reader = MindReader(path)
    reader.load()
    for snapshot in reader.read_snapshots():
        pass
