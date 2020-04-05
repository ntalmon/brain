import time

from brain.cli.client import run_cli
from brain.utils.connection import Connection
from brain.thought import Thought


def upload_thought(address, user, thought):
    address = (address[0], int(address[1]))
    user = int(user)
    t = int(time.time())
    thought_obj = Thought(user, t, thought)
    data = thought_obj.serialize()
    with Connection.connect(*address) as connection:
        connection.send(data)
    print('done')


if __name__ == '__main__':
    run_cli()
