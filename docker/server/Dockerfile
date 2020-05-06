FROM python:3.8
ADD brain /brain
ADD config /config
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN mkdir -p /brain-data
CMD ["python", "-m", "brain.server", "run-server", "rabbitmq://localhost:5672"]