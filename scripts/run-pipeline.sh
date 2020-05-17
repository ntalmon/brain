#!/usr/bin/env bash
# TODO: find how to get rid of --network host
# TODO: handle path running script from

set -e
echo "Building docker images"
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
sleep 5

echo "Starting project containers"
docker run --log-driver=journald -d --network host -v brain-volume:/brain-data --rm --name "brain-server" brain-server &
docker run --log-driver=journald -d --network host -v brain-volume:/brain-data --rm --name "brain-saver" brain-saver &
docker run --log-driver=journald -d --network host -v brain-volume:/brain-data --rm --name "brain-color-image" brain-color-image &
docker run --log-driver=journald -d --network host -v brain-volume:/brain-data --rm --name "brain-depth-image" brain-depth-image &
docker run --log-driver=journald -d --network host -v brain-volume:/brain-data --rm --name "brain-feelings" brain-feelings &
docker run --log-driver=journald -d --network host -v brain-volume:/brain-data --rm --name "brain-pose" brain-pose &
docker run --log-driver=journald -d --network host -v brain-volume:/brain-data --rm --name "brain-api" brain-api &

wait
