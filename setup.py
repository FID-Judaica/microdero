import fastentrypoints
from setuptools import setup

setup(
    name='microdero',
    version='0.0',
    author='FID-Judaica, Goethe Universitätsbibliothek',
    license='MLP 2.0/EUPL 1.1',
    author_email='a.christianson@ub.uni-frankfurt.de',
    url='https://github.com/FID-Judaica/microdero.py',
    description='deromanize as a ReSTful microservice',
    # long_description=open('README.rst').read(),
    packages=['microdero'],
    install_requires=[
        'deromanize',
        'aiohttp',
        'PyYaml'],
)
