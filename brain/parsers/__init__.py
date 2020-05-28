"""
The parsers package contains:

- A framework to detect registered parsers and be able to run them.
- The parsers themselves.
- Invocation of parser as a service.
"""

from .parsers import run_parser, invoke_parser, get_parsers
