import socket


class Connection:
    def __init__(self, sock):
        self.socket = sock

    def __repr__(self):
        s_name = ':'.join([str(attr) for attr in self.socket.getsockname()])
        p_name = ':'.join([str(attr) for attr in self.socket.getpeername()])
        return f'<Connection from {s_name} to {p_name}>'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @classmethod
    def connect(cls, host, port):
        sock = socket.socket()
        sock.connect((host, port))
        return Connection(sock)

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, size):
        data = b''
        while len(data) < size:
            packet = self.socket.recv(size - len(data))
            if not packet:
                raise Exception('Incomplete data')
            data += packet
        return data

    def close(self):
        self.socket.close()
