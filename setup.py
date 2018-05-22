from setuptools import setup, find_packages

setup(
    name='PyTOR',
    version='1.0.0',
    description='A small library that allows you to easily download a list of Official TOR output servers, '
                'and return it in a convenient and accessible way. ',
    packages=find_packages(exclude=["example"]),
    install_requires=[
        "requests"
    ]
)
