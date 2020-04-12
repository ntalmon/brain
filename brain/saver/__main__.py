import sys

if __name__ == '__main__':
    from brain.cli.saver import run_cli

    try:
        run_cli()
    except Exception as error:
        print(f'ERROR: {error}')
        sys.exit(1)
