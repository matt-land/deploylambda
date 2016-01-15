#!/usr/bin/env python
import deploylambda
import os
import subprocess
import sys


def deploy():
    deploylambda.setupOS()

    try:
        sys.argv[1]
    except:
        deploylambda.print_lambdas()
        exit(1)

    lambda_name = sys.argv[1]
    deploylambda.backup_old_lambda(lambda_name)
    zipname = deploylambda.create_zip(lambda_name)
    deploylambda.deploy_new_lambda(lambda_name)
    exit(0)

def package():
    deploylambda.setupOS()
    try:
        sys.argv[1]
    except:
        deploylambda.print_lambdas()
        exit(1)

    lambda_name = sys.argv[1]
    zipname = deploylambda.create_zip(lambda_name)
    exit(0)

def backup():
    deploylambda.setupOS()
    try:
        sys.argv[1]
    except:
        deploylambda.print_lambdas()
        exit(1)
    lambda_name = sys.argv[1]
    deploylambda.backup_old_lambda(lambda_name)
    exit(0)

def list():
    deploylambda.setupOS()
    deploylambda.print_lambdas()