from setuptools import setup, find_packages

setup(
    name='Brain',
    version='0.1.0',
    author='Noam Talmon',
    description='Advanced System Design - Final Project',
    packages=find_packages(),
    install_requires=['click'],
    tests_require=['pytest', 'pytest-cov']
)
