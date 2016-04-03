from setuptools import setup

from os import path


def readme():
    with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst'), encoding="utf8") as f:
        return f.read()

setup(
    name='ionflowscript',
    version='0.0.1',
    packages=['ionflowscript'],
    url='https://github.com/bcaller/ionflowscript',
    entry_points={
        'console_scripts': [
            'ionflowscript = ionflowscript.__main__:main'
        ]
    },
    license='GPLv3',
    author='Ben Caller',
    author_email='bcaller [at] gmail dot com',
    long_description=readme(),
    description='Read Ion Torrent flow scripts controlling your sequencer\'s fluidics in a more friendly format'
)
