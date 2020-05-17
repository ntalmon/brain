FROM python:3.8
COPY brain /brain
COPY config /config
COPY scripts/wait-for-it.sh /
COPY scripts/build.sh /
COPY requirements.txt /
EXPOSE 8000
RUN apt-get update -y
RUN pip install -r requirements.txt
RUN ./build.sh