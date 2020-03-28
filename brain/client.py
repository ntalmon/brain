import time

from brain.cli import CommandLineInterface
from brain.utils.connection import Connection
from brain.thought import Thought

cli = CommandLineInterface()


@cli.command
def upload_thought(address, user, thought):
    address = (address[0], int(address[1]))
    user = int(user)
    n = len(thought)
    t = int(time.time())
    thought_obj = Thought(user, t, thought)
    data = thought_obj.serialize()
    with Connection.connect(*address) as connection:
        connection.send(data)
    print('done')


if __name__ == '__main__':
    import sys

    sys.exit(cli.main())
