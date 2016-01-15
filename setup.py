#!/usr/bin/env python

from setuptools import setup

setup(name='deploylambda',
    version='0.12',
    description='Package and deploy aws lambda functions, and backup current versions',
    url='http://github.com/matt-land/deploy-lambda',
    author='Matt Land',
    author_email='mwfrankland@gmail.com',
    license='MIT',
    classifiers= [
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.6',
      'Programming Language :: Python :: 2.7',
    ],
    install_requires=['boto', 'wget'],
    packages=['deploylambda'],
    entry_points={
          'console_scripts': [
              'deploy-lambda=deploylambda.command_line:deploy',
              'backup-lambda=deploylambda.command_line:backup',
              'list-lambda=deploylambda.command_line:list',
          ]
    },
)
