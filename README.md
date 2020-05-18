# Advanced System Design - Final Project
[![Build Status](https://travis-ci.org/noamtau1/brain.svg?branch=master)](https://travis-ci.org/noamtau1/brain)
[![codecov](https://codecov.io/gh/noamtau1/brain/branch/master/graph/badge.svg)](https://codecov.io/gh/noamtau1/brain)

# Brain
Final project of Advanced System Design. See [full documentation](https://brain.readthedocs.io/en/latest/).

## Installation
1. Clone the repository and enter it:

    ```bash
    $ git clone git@github.com:noamtau1/brain.git
    ...
    $ cd brain/
    ```
2. Run the installation script and activate the virtual environment:
    ```bash
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [brain] $ # you're good to go!
    ```
3. To check that everything is working as expected, run the tests:
    ```bash
    $ # start docker containers for mongodb and rabbitmq
    $ pytest tests/
    ...
    ```

## Usage
### Client
The client is available in `brain.client` with the following interface:
```python
from brain.client import upload_sample
upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
```
It will read the snapshots from the given `path`, and stream them to the server with the given `host` and `port`.

The client is also available with the following CLI:
```bash
$ python -m brain.client upload-sample \
    -h/--host '127.0.0.1'              \
    -p/--port 8000                     \
    'sample.mind.gz'
```
### Server
The server is available in `brain.server` with the following interface:
```python
from brain.server import run_server
def print_message(message):
    print(message)
run_server(host='127.0.0.1', port=8000, publish=print_message)
```
It will listen on `host`:`port` and pass received messages to `publish` 

The server is also available with the following CLI:
```bash
$ python -m brain.server run-server \
    -h/--host '127.0.0.1'           \
    -p/--port 8000                  \
    'rabbitmq://127.0.0.1:5672'
```
Using the CLI, the server will publish the received snapshots to a message queue at the given address.
### Parsers
The parsers are available in `brain.parsers` with the following interface:
```python
from brain.parsers import run_parser
data = ...
result = run_parser('pose', data)
```
It will run the parser with the given data (as consumed from the message queue)
and return the result.

The parsers are also available with the following CLI:
```bash
$ python -m brain.parsers parse 'pose' 'snapshot.raw' > 'pose.result'
$ python -m brain.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672'
```
- `parse` will run the parser with with data in the given file, and print the result.
- `run-parser` will run the parser as a service, i.e. it will consume the message queue at \
the given address, parse incoming messages, and publish the results back to the queue.
#### Available parsers
- `pose` - collects the translation and the rotation of the users's head at a given timestamp.
- `color_image` - collects the color image of what the user was seeing at a given timestamp.
- `depth_image` - collects the depth image of what the user was seeing at a given timestamp.
- `feelings` - collects the feelings that the user was experiencing at any timestamp.
#### Adding a new parser
Let's say we want to add a new parser that parses what the user hears. We will call it sound parser. \
At first we will add a new file to the parsers package:
```bash
$ touch parsers/sound.py
```
The parser can expose its parsing function in several ways:
- As a function:
  ```python
  def parse_sound(data):
      # Parse the data
      ...
      return result
  parse_sound.field = 'sound'
  ```
  The important things to keep in mind are the `parse_` prefix and the `.field` which is the name of the parser.
- As a class:
  ```python
  class SoundParser:
      field = 'sound'
      def parse(self, data):
          # Parse the data
          ...
          return result
  ```
  The important things to keep in mind are the 'Parser' suffix, the `field` and the `parse` method.
### Saver
The saver is available in `brain.saver` with the following interface:
```python
from brain.saver import Saver
saver = Saver(database_url)
data = ...
saver.save('pose', data)
```
It will connect to the database at `database_url`, and save the given `data` under the given `topic` to the database.

The saver is also available with the following CLI:
```bash
$ python -m brain.saver save                    \
    -d/--database 'mongodb://127.0.0.1:27017'   \
    'pose'                                      \
    'pose.result'
$ python -m brain.saver run-saver   \
    'mongodb://127.0.0.1:27017'     \
    'rabbitmq://127.0.0.1:5672'
```
- `save` accepts a topic name and a path to some raw data, as consumed from the message queue, \
    and saves it to a database.
- `run-saver` will run the saver as a service, i.e. it will consume the message queue, and save \
    incoming messages to the database.