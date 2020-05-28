"""
The saver package gets parsed results and saves them to a database. It also allows to run the saver as a service
that consumes the results from MQ.
"""

from .saver import Saver, run_saver
