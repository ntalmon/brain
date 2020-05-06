# TODO: pass logic to docker file
# TODO: find how to get rid of --network host
# TODO: handle path running script from

set -e
echo "Building docker images"
docker build -f docker/api/Dockerfile . -t brain-api &
docker build -f docker/color_image/Dockerfile . -t brain-color-image &
docker build -f docker/depth_image/Dockerfile . -t brain-depth-image &
docker build -f docker/feelings/Dockerfile . -t brain-feelings &
docker build -f docker/gui/Dockerfile . -t brain-gui &
docker build -f docker/pose/Dockerfile . -t brain-pose &
docker build -f docker/saver/Dockerfile . -t brain-saver &
docker build -f docker/server/Dockerfile . -t brain-server &
wait

echo "Stop running containers"
set +e
docker container stop brain-rabbitmq
docker container stop brain-mongo
set -e

echo "Starting rabbitmq container"
docker run -d -p 5672:5672 --rm --name brain-rabbitmq rabbitmq
echo "Starting mongodb container"
docker run -d -p 27017:27017 --rm --name brain-mongo mongo
sleep 5

echo "Starting project containers"
docker run -d --network host --rm --name "brain-server" brain-server &
docker run -d --network host --rm --name "brain-saver" brain-saver &
docker run -d --network host --rm --name "brain-color-image" brain-color-image &
docker run -d --network host --rm --name "brain-depth-image" brain-depth-image &
docker run -d --network host --rm --name "brain-feelings" brain-feelings &
docker run -d --network host --rm --name "brain-pose" brain-pose &

wait
