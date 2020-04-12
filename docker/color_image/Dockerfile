FROM python:3.8
ADD brain /brain
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "-m", "brain.parsers", "run-parser", "color-image", "rabbitmq://127.0.0.1:5672"]