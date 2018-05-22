from setuptools import *

setup(
    name='bstockimages',
    version='0.1',
    description='Utilities to help find, download, and manage images.',
    author='Michael Gorlin',
    license='MIT',
    packages=['bstockimages'],
    install_requires=[
        'requests',
        'pymongo',
        'lxml',
        'bottlenose',
    ]
)
