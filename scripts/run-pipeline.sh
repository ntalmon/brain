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
docker container stop brain-server brain-saver brain-color-image brain-depth-image brain-feelings brain-pose brain-gui \
  brain-api brain-rabbitmq brain-mongo
set -e

echo "Starting rabbitmq container"
docker run -d -p 5672:5672 --rm --name brain-rabbitmq rabbitmq
echo "Starting mongodb container"
docker run -d -p 27017:27017 --rm --name brain-mongo mongo
sleep 5

sudo rm -rf /tmp/brain-data
mkdir /tmp/brain-data

echo "Starting project containers"
docker run --log-driver=journald -d --network host -v /tmp/brain-data:/brain-data --rm --name "brain-server" brain-server &
docker run --log-driver=journald -d --network host -v /tmp/brain-data:/brain-data --rm --name "brain-saver" brain-saver &
docker run --log-driver=journald -d --network host -v /tmp/brain-data:/brain-data --rm --name "brain-color-image" brain-color-image &
docker run --log-driver=journald -d --network host -v /tmp/brain-data:/brain-data --rm --name "brain-depth-image" brain-depth-image &
docker run --log-driver=journald -d --network host -v /tmp/brain-data:/brain-data --rm --name "brain-feelings" brain-feelings &
docker run --log-driver=journald -d --network host -v /tmp/brain-data:/brain-data --rm --name "brain-pose" brain-pose &
docker run --log-driver=journald -d --network host -v /tmp/brain-data:/brain-data --rm --name "brain-api" brain-api &

wait
