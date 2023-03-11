import probablefutures
from setuptools import setup

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='probablefutures',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=probablefutures.__version__,
    packages=['probablefutures'],
    url='',
    license='',
    author='jeffd',
    author_email='jeffdo@gmail.com',
    description='Probable Futures Python API '
)
