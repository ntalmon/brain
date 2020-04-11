import yaml

from brain import config_path

client_config_file = config_path / 'client.yml'
with open(str(client_config_file), 'r') as reader:
    client_config = yaml.load(reader, Loader=yaml.Loader)
