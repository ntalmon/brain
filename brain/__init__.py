"""
TODO: handle network faults and exceptions
TODO: mq to not auto ack
TODO: add framework for agents drivers
TODO: complete logging
TODO: make parsers in thread
"""
import pathlib

project_path = pathlib.Path(__file__).parent.parent
app_path = project_path / 'app'
brain_path = project_path / 'brain'
config_path = project_path / 'config'
data_path = project_path / 'brain-data'
log_path = project_path / 'brain.log'
tests_path = project_path / 'tests'  # TODO: should this stay here?
