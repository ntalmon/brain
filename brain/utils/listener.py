import socket

from brain.utils.connection import Connection


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.socket = socket.socket()
        if reuseaddr:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))

    def __repr__(self):
        return f'Listener(port={self.port}, host={self.host!r}, ' \
               f'backlog={self.backlog}, reuseaddr={self.reuseaddr})'

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        self.socket.listen(self.backlog)

    def stop(self):
        self.socket.close()

    def accept(self):
        c, _ = self.socket.accept()
        return Connection(c)
