#!/usr/bin/env python
import deploylambda
import os
import subprocess
import sys


def getfirstarg():
    try:
        sys.argv[1]
    except:
        deploylambda.print_lambdas()
        exit(1)
    return sys.argv[1]


def deploy():
    deploylambda.setupOS()
    lambda_name = getfirstarg()
    deploylambda.backup_old_lambda(lambda_name)
    deploylambda.create_zip(lambda_name)
    deploylambda.deploy_new_lambda(lambda_name)
    exit(0)


def update():
    deploylambda.setupOS()
    lambda_name = getfirstarg()
    deploylambda.deploy_new_lambda(lambda_name)
    exit(0)


def package():
    deploylambda.setupOS()
    lambda_name = getfirstarg()
    deploylambda.create_zip(lambda_name)
    exit(0)


def backup():
    deploylambda.setupOS()
    lambda_name = getfirstarg()
    deploylambda.backup_old_lambda(lambda_name)
    if not os.path.isfile('./'+lambda_name):
        deploylambda.unpack_lamdba(lambda_name)
    exit(0)


def list():
    deploylambda.setupOS()
    deploylambda.print_lambdas()
    exit(0)


def unpack():
    deploylambda.setupOS()
    lambda_name = getfirstarg()
    deploylambda.unpack_lamdba(lambda_name)