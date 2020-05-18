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
The client is available as `brain.client` as container the following interface:
```python
from brain.client import upload_sample
upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
```
It will read the snapshots from the given file, and stream them to the server with the given host and port.

Or with the following CLI:
```bash
$ python -m brain.client upload-sample \
    -h/--host '127.0.0.1'              \
    -p/--port 8000                     \
    'sample.mind.gz'
```