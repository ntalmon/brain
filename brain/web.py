import os
import datetime
from brain.website import Website

_data_dir = ''
website = Website()

_INDEX_HTML = '''
<html>
    <head>
    </head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''

_USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a/></li>
'''

_USER_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <table>
            {thoughts}
        </table>
    </body>
</html>
'''

_THOUGHT_HTML = '''
<tr>
    <td>{timestamp}</td>
    <td>{thought}</td>
</tr>
'''


@website.route('/')
def route_index():
    users_html = []
    users = os.listdir(_data_dir)
    for user in users:
        users_html.append(_USER_LINE_HTML.format(user_id=user))
    index_html = _INDEX_HTML.format(users='\n'.join(users_html))
    return 200, index_html


@website.route('/users/([0-9]+)')
def route_user(user_id):
    users = os.listdir(_data_dir)
    if str(user_id) not in users:
        return 400, ''
    user_dir = os.path.join(_data_dir, user_id)
    thoughts = os.listdir(user_dir)
    thoughts_html = []
    for fname in thoughts:
        with open(os.path.join(user_dir, fname), 'r') as file:
            ts = datetime.datetime.strptime(fname, "%Y-%m-%d_%H-%M-%S.txt").strftime("%Y-%m-%d %H:%M:%S")
            thought = _THOUGHT_HTML.format(timestamp=ts, thought=file.read())
            thoughts_html.append(thought)
    data = _USER_HTML.format(user_id=user_id, thoughts='\n'.join(thoughts_html))
    return 200, data


def run_webserver(addr, data_dir):
    global _data_dir
    _data_dir = data_dir
    website.run(addr)


def main(argv):
    global data_dir

    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <data_dir>')
        return 1
    try:
        addr = argv[1]
        addr = addr.split(':')
        if len(addr) != 2:
            raise Exception("Invalid address format given, expected ip_address:port")
        addr = (addr[0], int(addr[1]))
        data_dir = argv[2]
        run_webserver(addr, data_dir)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys

    data_dir = ''
    sys.exit(main(sys.argv))
