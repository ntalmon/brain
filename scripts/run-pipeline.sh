#!/usr/bin/env bash
# TODO: find how to get rid of --network host
# TODO: handle path running script from

set -e
./scripts/build.sh docker

echo "Stop running containers"
set +e
docker container stop brain-server brain-saver brain-color-image brain-depth-image brain-feelings brain-pose brain-gui \
  brain-api brain-rabbitmq brain-mongo
docker volume rm brain-volume

set -e
docker volume create --name brain-volume
echo "Starting rabbitmq container"
docker run -d -p 5672:5672 --rm --name brain-rabbitmq rabbitmq
echo "Starting mongodb container"
docker run -d -p 27017:27017 --rm --name brain-mongo mongo

./scripts/wait-for-it.sh 127.0.0.1:5672

echo "Starting containers"
docker run -d --network host -v brain-volume:/brain-data --rm --name "brain-server" brain-server &
docker run -d --network host -v brain-volume:/brain-data --rm --name "brain-saver" brain-saver &
docker run -d --network host -v brain-volume:/brain-data --rm --name "brain-color-image" brain-color-image &
docker run -d --network host -v brain-volume:/brain-data --rm --name "brain-depth-image" brain-depth-image &
docker run -d --network host -v brain-volume:/brain-data --rm --name "brain-feelings" brain-feelings &
docker run -d --network host -v brain-volume:/brain-data --rm --name "brain-pose" brain-pose &
docker run -d --network host -v brain-volume:/brain-data --rm --name "brain-api" brain-api &
docker run -d --network host -v brain-volume:/brain-data --rm --name "brain-gui" brain-gui &
wait

./scripts/wait-for-it.sh 127.0.0.1:8000