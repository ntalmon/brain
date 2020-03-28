import struct
import os
import datetime
import threading

from brain.cli import CommandLineInterface
from brain.utils.listener import Listener

cli = CommandLineInterface()


class ThreadHandleClient(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection, data_dir):
        threading.Thread.__init__(self)
        self.connection = connection
        self.data_dir = data_dir

    def run(self):
        hdr = self.connection.receive(20)
        uid, ts, sz = struct.unpack('LLI', hdr)
        thought = self.connection.receive(sz)
        thought = thought.decode()
        fname = '{}.txt'.format(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S'))
        u_path = os.path.join(self.data_dir, str(uid))
        self.lock.acquire()
        if not os.path.isdir(u_path):
            os.mkdir(u_path)
        f_path = os.path.join(u_path, fname)
        mode = 'w'
        if os.path.isfile(f_path):
            mode = 'a'
            thought = '\n' + thought
        with open(f_path, mode) as file:
            file.write(thought)
        self.lock.release()


@cli.command
def run(address, data_dir):
    address = address.split(':')
    if len(address) != 2:
        raise Exception("Invalid address format given, expected ip_address:port")
    address = (address[0], int(address[1]))
    with Listener(address[0], host=address[0]) as listener:
        while True:
            connection = listener.accept()
            c_thread = ThreadHandleClient(connection, data_dir)
            c_thread.start()


if __name__ == '__main__':
    import sys

    sys.exit(cli.main())
