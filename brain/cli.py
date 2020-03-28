import inspect
import sys


class CommandLineInterface:
    def __init__(self):
        self.funcs = {}
        self.params = {}

    def command(self, f):
        self.funcs[f.__name__] = f
        self.params[f.__name__] = inspect.getfullargspec(f)
        return f

    def main(self):
        argv = sys.argv
        if len(argv) < 2:
            print(f'USAGE: python {argv[0]} <command> [<key>=<value>]*')
            sys.exit(1)
        cmd = argv[1]
        if cmd not in self.funcs:
            print('Invalid command')
            print(f'USAGE: python {argv[0]} <command> [<key>=<value>]*')
            sys.exit(1)
        func = self.funcs[argv[1]]
        params = self.params[argv[1]]
        args = argv[2:]
        args_list = []
        kwargs_dict = {}
        start_optional = len(params.args or []) - len(params.defaults or [])
        for arg in args:
            splt = arg.split('=', maxsplit=1)
            if len(splt) < 2:
                print('Invalid format')
                print(f'USAGE: python {argv[0]} <command> [<key>=<value>]*')
                sys.exit(1)
            key, val, = splt
            if key in params.args:
                if params.args.index(key) < start_optional:
                    args_list.append(val)
                else:
                    kwargs_dict[key] = val
            else:
                print('Invalid arguments')
                print(f'USAGE: python {argv[0]} <command> [<key>=<value>]*')
                sys.exit(1)
        try:
            func(*args_list, **kwargs_dict)
        except Exception as error:
            print(f'ERROR: {error}')
        sys.exit(0)
