#!/usr/bin/env python

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
        name='deploylambda',
        version='0.12',
        description='Package and deploy aws lambda functions, and backup current versions',
        url='http://github.com/matt-land/deploy-lambda',
        author='Matt Land',
        author_email='mwfrankland@gmail.com',
        license='MIT',
        classifiers=[
          'Programming Language :: Python :: 2.7',
        ],
        install_requires=['boto', 'wget'],
        packages=['deploylambda'],
        entry_points={
              'console_scripts': [
                  'deploy-lambda=deploylambda.command_line:deploy',
                  'package-lambda=deploylambda.command_line:package',
                  'backup-lambda=deploylambda.command_line:backup',
                  'list-lambda=deploylambda.command_line:list',
                  'unpack-lambda=deploylambda.command_line:unpack',
                  'update-lambda=deploylambda.command_line:update',
              ]
        },
)
