FROM python:3.8
ADD brain /brain
ADD config /config
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "-m", "brain.saver", "run-saver", "mongodb://127.0.0.1:27017", "rabbitmq://127.0.0.1:5672"]