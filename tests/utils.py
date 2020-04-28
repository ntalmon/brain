import subprocess

from google.protobuf import json_format


def execute_command(command, safety=False):
    sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    code, out, err = sp.returncode, sp.stdout.read(), sp.stderr.read()
    if safety:
        assert code == 0, f'Error while executing command: command={command}, exit-code={code}'
    return code, out, err


def protobuf2dict(x):
    return json_format.MessageToDict(x, including_default_value_fields=True, preserving_proto_field_name=True)


def cmp_protobuf(x, y):
    dict_x = protobuf2dict(x)
    dict_y = protobuf2dict(y)
    return dict_x == dict_y
