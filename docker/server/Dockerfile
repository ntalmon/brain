FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y python3.8 python3-pip
ADD ../../requirements.txt /requirements.txt
CMD ["python", "-m", "brain.server", "-h", "127.0.0.1", "-p", "8000", "rabbitmq://127.0.0.1:5672"]