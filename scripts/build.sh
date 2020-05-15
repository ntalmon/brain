#!/usr/bin/env bash

python -m grpc_tools.protoc -I brain/protobuf/ --python_out=brain/autogen reader.proto
python -m grpc_tools.protoc -I brain/protobuf/ --python_out=brain/autogen protocol.proto
python -m grpc_tools.protoc -I brain/protobuf/ --python_out=brain/autogen parsers.proto