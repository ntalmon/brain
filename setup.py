import subprocess

from setuptools import setup, find_packages
from setuptools.command.install import install


def execute_command(command):
    sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    code, out, err = sp.returncode, sp.stdout.read(), sp.stderr.read()
    return code, out, err


class InstallCommand(install):
    def run(self):
        code, out, err = execute_command(['python', '-m', './scripts/build.sh', 'protobuf'])
        if code != 0:
            raise Exception(f'Failed to build protobuf: out={out}, err={err}')
        install.run(self)


setup(
    name='Brain',
    version='0.1.0',
    author='Noam Talmon',
    cmdclass={'install': InstallCommand},
    description='Advanced System Design - Final Project',
    packages=find_packages(),
    install_requires=['click'],
    tests_require=['pytest', 'pytest-cov']
)
