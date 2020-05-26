"""
This package contains the API for brain.
It is RESTful API that reflects the data stored in the database in multiple entry points.
It provides the following interface under brain.api:
    - run_api_server(host='127.0.1', port=5000, database_url='mongodb://127.0.0.1:27017')
"""
from .api import run_api_server
