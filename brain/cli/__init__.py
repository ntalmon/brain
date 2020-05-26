"""
CLI for brain. The CLI simply reflect the API with the following commands:
    - get-users: get all users
    - get-user: get a specific user
    - get-snapshots: get all snapshots of a user
    - get-snapshot: get a specific snapshot of a user
    - get-result: get a specific parsing result of a snapshot

Each command will query the API and print the retrieved response.
All command are available under brain.cli (python -m brain.cli ...)
and accepts to addition parameters:
    - -h/--host: hostname of the API server
    - -p/--port: port number of the API server.
The get-result command also accepts the -s/--save flag, that if specified,
it received a path and saves the result's data to that path.

For example:
    python -m brain.api get-snapshot 1 2 -h '127.0.0.1' -p 5000

TODO: implement -s/--save for get-result
"""
