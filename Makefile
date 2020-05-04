all:
	protoc -I./brain/protobuf --python_out=brain/autogen brain/protobuf/*.proto
clean:
	rm -rf brain/autogen/*