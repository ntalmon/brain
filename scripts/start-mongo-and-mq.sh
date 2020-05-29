#!/usr/bin/env bash

docker container stop brain-rabbitmq brain-mongo
docker run -d -p 5672:5672 --rm --name brain-rabbitmq rabbitmq
docker run -d -p 27017:27017 --rm --name brain-mongo mongo