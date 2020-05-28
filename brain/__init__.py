"""
The basic idea of the brain project is to build python-based, software-only implementation of a
`Brain Computer Interface <https://en.wikipedia.org/wiki/Brain%E2%80%93computer_interface>`_.
The real client and hardware will be replace by a sample file contains cognition snapshots.

Basic flow - upload snapshots
=============================
The client reads the sample file and streams the snapshots one by one to the server.
The server the receives snapshots, and sends them to different parsers using a message queue.
The parsers are parsing the snapshots and send the results to the saver using the message queue.
The saver receives parsed snapshots (snapshots + parsing results) and saves them to the database.

Read the uploaded data
======================
There are several ways to get the uploaded data:

* The API - RESTful API for getting data from the database (users, snapshots, results, etc.).
* The CLI - command line interface for the API.
* The GUI - reflects the API and presents the uploaded data.

TODO: make sure there are comments.
TODO: make sure there are type annotations.
"""

import pathlib

project_path = pathlib.Path(__file__).parent.parent
app_path = project_path / 'app'
brain_path = project_path / 'brain'
config_path = project_path / 'config'
data_path = project_path / 'brain-data'
log_path = project_path / 'brain.log'
tests_path = project_path / 'tests'
