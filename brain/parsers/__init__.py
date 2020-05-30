"""
The parsers package contains:

- A framework to detect registered parsers and be able to run them.
- The parsers themselves.
"""

from .framework import run_parser, invoke_parser, get_parsers
