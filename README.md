# Advanced System Design - Final Project
[![Build Status](https://travis-ci.org/noamtau1/brain.svg?branch=master)](https://travis-ci.org/noamtau1/brain)
[![codecov](https://codecov.io/gh/noamtau1/brain/branch/master/graph/badge.svg)](https://codecov.io/gh/noamtau1/brain)

# Brain
Final project of Advanced System Design. See [full documentation](https://brain.readthedocs.io/en/latest/).

The basic idea of the project is to build python-based, software-only implementation
of [Brain Computer Interface](https://en.wikipedia.org/wiki/Brain%E2%80%93computer_interface). \
The real client and hardware will be replace by a sample file contains cognition snapshots.
#### Basic flow - upload snapshots
1. The client reads the sample file and streams the snapshots one by one to the server.
2. The server the receives snapshots, and sends them to different parsers using a message queue.
3. The parsers are parsing the snapshots and send the results to the saver using the message queue.
4. The saver receives parsed snapshots (snapshots + parsing results) and saves them to the database.
#### Read the uploaded data
There are several ways to get the uploaded data:
- The API - RESTful API for getting data from the database (users, snapshots, results, etc.).
- The CLI - command line interface for the API.
- The GUI - reflects the API and presents the uploaded data.

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
    ```
3. Run the build script to build everything required before running the tests:
    ```bash
    [brain] $ ./scripts/build.sh tests
    ```
4. To check that everything is working as expected, run the tests:
    ```bash
    [brain] $ pytest tests/
    ...
    ```
## Deployment
Each one of the services can also run from a container.
In order to build and start all the containers, you should run:
```bash
$ ./scripts/run-pipeline.sh
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

### API
The API is available in `brain.api` with the following interface:
```python
from brain.api import run_api_server
run_api_server(
    host='127.0.1',
    port=5000,
    database_url='mongodb://127.0.0.1:27017'
)
```
It will listen on `host`:`port` and serve data from database_url.

The API is also available with the following CLI:
```bash
$ python -m brain.api run-server    \
    -h/--host '127.0.0.1'           \
    -p/--port 5000                  \
    -d/--database 'mongodb://127.0.0.1:27017'
```
The API is RESTful API and supports the following endpoints:
- `GET /users` \
    Returns the list of all supported users, including their IDs and names only.
- `GET/users/<user-id>` \
    Returns the specified users' details: ID, name, birthday and gender.
- `GET /users/<user-id>/snapshots` \
    Returns the list of the specified user's snapshot IDs and datetimes only.
- `GET /users/<user-id>/snapshots/<snapshot-id>` \
    Returns the specified snapshot's details: ID, datetime, and the available results' \
     names only (e.g. **pose**).
- `GET /users/<user-id>/snapshots/<snapshot-id>/<result-name>` \
    Returns the specified snapshot's result in JSON format. \
    For some parse results that contain large binary files (like **color_image** and **depth_image**), \
    the blob will be saved into the disk, and the result will contain the file path.
    The file data is available the following URL: \
    `GET /users/<user-id>/snapshots/<snapshot-id>/<result-name>/data`.

### CLI
The CLI consumes and reflects the API and contains the following commands:
```bash
$ python -m brain.cli get-users
$ python -m brain.cli get-user USER_ID
$ python -m brain.cli get-snapshots USER_ID
$ python -m brain.cli get-snapshot USER_ID SNAPSHOT_ID
$ python -m brain.cli get-result USER_ID SNAPSHOT_ID RESULT_NAME
```
All commands accept the `-h/--host` and `-p/--port` flags to configure the host and port of the API.

### GUI
The GUI is consumes the API and reflects the retrieved data. \
It is available in `brain.gui` with the following interface:
```python
from brain.gui import run_server
run_server(
    host='127.0.0.1',
    port=8080,
    api_host='127.0.0.1',
    api_port=5000
)
```
The GUI is also available with the following CLI:
```bash
$ python -m brain.gui run-server    \
    -h/--host '127.0.0.1'           \
    -p/--port 8080                  \
    -H/--api-host '127.0.0.1'       \
    -P/--api-port 5050
```