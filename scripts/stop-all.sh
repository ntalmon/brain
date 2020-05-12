#!/usr/bin/env bash

echo "Stopping all containers"
docker container stop brain-server brain-saver brain-color-image brain-depth-image brain-feelings brain-pose brain-gui \
  brain-api brain-rabbitmq brain-mongo
docker volume rm brain-volume
