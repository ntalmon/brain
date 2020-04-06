class Saver:
    def __init__(self, database_url):
        self.database_url = database_url

    def save(self, parser, data):
        pass


if __name__ == '__main__':
    from brain.cli.saver import run_cli

    run_cli()
