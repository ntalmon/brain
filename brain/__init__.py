"""
TODO: handle network faults and exceptions
TODO: create data dir
TODO: mq to not auto ack
TODO: client registration (optional)
TODO: add framework for agents drivers
TODO: parsers framework to support classes
"""
import pathlib

project_path = pathlib.Path(__file__).parent.parent  # TODO: is it a good practice?
brain_path = project_path / 'brain'
config_path = project_path / 'config'
data_path = project_path / 'brain-data'
tests_path = project_path / 'tests'
