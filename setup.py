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
        install_requires=['wget'],
        packages=['deploylambda'],
        entry_points={
              'console_scripts': [
                  'package-venv-lambda=deploylambda.command_line:package_venv_lambda',
                  'deploy-lambda=deploylambda.command_line:deploy_lambda',
                  'package-lambda=deploylambda.command_line:package_lambda',
                  'backup-lambda=deploylambda.command_line:backup_lambda',
                  'list-lambda=deploylambda.command_line:list_lambda',
                  'unpack-lambda=deploylambda.command_line:unpack_lambda',
                  'update-lambda=deploylambda.command_line:update_lambda',
                  'metadata-lambda=deploylambda.command_line:metadata_lambda',
                  'alias-lambda=deploylambda.command_line:alias_lambda',
                  'promote-lambda=deploylambda.command_line:promote_lambda',
              ]
        },
)
