#!/usr/bin/env bash

usage() {
	echo "Usage: build.sh [COMMANDS]..."
	echo "Commands:"
	echo "	protobuf (compile .proto files)"
	echo "	docker (build docker images)"
	echo "	app (build react app)"
}

build_protobuf() {
	python -m grpc_tools.protoc -I brain/protobuf/ --python_out=brain/autogen reader.proto
	python -m grpc_tools.protoc -I brain/protobuf/ --python_out=brain/autogen protocol.proto
	python -m grpc_tools.protoc -I brain/protobuf/ --python_out=brain/autogen parsers.proto
}

build_docker() {
	docker build -f docker/common . -t brain-common
	docker build -f docker/api . -t brain-api &
	docker build -f docker/color_image . -t brain-color-image &
	docker build -f docker/depth_image . -t brain-depth-image &
	docker build -f docker/feelings . -t brain-feelings &
	docker build -f docker/gui . -t brain-gui &
	docker build -f docker/pose . -t brain-pose &
	docker build -f docker/saver . -t brain-saver &
	docker build -f docker/server . -t brain-server &
	wait
}

build_app() {
	npm install --prefix app/
	npm run --prefix app/ build
}

if [[ $# -eq 0 ]] ; then
	usage
else
	mkdir -p brain-data
	for command in "$@"; do
		if [[ "$command" == "protobuf" ]]; then
			build_protobuf
		elif [[ "$command" == "docker" ]]; then
			build_docker
		elif [[ "$command" == "app" ]]; then
			build_app
		fi
	done
fi
exit 0