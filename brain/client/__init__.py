"""
The client package is responsible for reading snapshots from sample file and stream them one by one to the server.
It provides the following interface:

.. code-block:: python

    from brain.client import upload_sample
    upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
"""
from .client import upload_sample
