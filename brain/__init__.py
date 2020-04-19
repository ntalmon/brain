"""
TODO: is it a good practice?
TODO: handle network faults and exceptions
TODO: create data dir
TODO: mq to not auto ack
TODO: client registration (optional)
TODO: add framework for agents drivers
"""
import pathlib

project_path = pathlib.Path(__file__).parent.parent
brain_path = project_path / 'brain'
config_path = project_path / 'config'
data_path = project_path / 'data'
tests_path = project_path / 'tests'
