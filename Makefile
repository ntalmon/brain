all:
# 	protoc -I./brain/protobuf --python_out=brain/autogen brain/protobuf/*.proto
	python -m grpc_tools.protoc -I brain/protobuf/ --python_out=brain/autogen reader.proto
	python -m grpc_tools.protoc -I brain/protobuf/ --python_out=brain/autogen protocol.proto
	python -m grpc_tools.protoc -I brain/protobuf/ --python_out=brain/autogen parsers.proto
clean:
	rm -rf brain/autogen/*_pb2.py brain/autogen/__pycache__