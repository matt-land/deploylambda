#!/usr/bin/env python

from setuptools import setup

setup(name='deploylambda',
    version='0.1',
    description='Deploy aws lambda code',
    url='http://github.com/matt-land/deploy-lambda',
    author='Matt Land',
    author_email='mwfrankland@gmail.com',
    license='MIT',
    packages='deploy-lambda',
    install_requires=['boto', 'wget', 'json', 'shutil', 'ziputil'],
    zip_safe=False)