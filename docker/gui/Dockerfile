FROM python:3.8
#FROM node:8.10.0
#ADD app /app
ADD brain /brain
ADD config /config
ADD requirements.txt /requirements.txt
#WORKDIR /app
#RUN npm run build
RUN pip install -r requirements.txt
# TODO: change to the right parameters
#CMD ["python", "-m", "brain.gui", "run-server", "-h", "127.0.0.1", "-p", "8080", "-H", "127.0.0.1", "-P", "5000"]