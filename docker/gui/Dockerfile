FROM python:3.8
ADD brain /brain
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt
# TODO: change to the right parameters
CMD ["python", "-m", "brain.gui", "run-server"]