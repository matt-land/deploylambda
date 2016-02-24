#!/usr/bin/env python
import deploylambda
import os
import subprocess
import sys
import argparse
from deploylambda import DeployLambda
parser = argparse.ArgumentParser(description='Deploy some lambdas')

parser.add_argument('--profile', help='specify an aws profile to use, if not the default', default='default')
parser.add_argument('lambda_name', nargs='?', help='lambda name')
args = parser.parse_args()


def deploy():
    global args
    d = DeployLambda(args.profile)
    d.backup_old_lambda(args.lambda_name)
    d.create_zip(args.lambda_name)
    d.deploy_new_lambda(args.lambda_name)
    exit(0)


def update():
    global args
    d = DeployLambda(args.profile)
    d.create_zip(args.lambda_name)
    d.deploy_new_lambda(args.lambda_name)
    exit(0)


def package():
    global args
    d = DeployLambda(args.profile)
    d.create_zip(args.lambda_name)
    exit(0)


def backup():
    global args
    d = DeployLambda(args.profile)
    d.backup_old_lambda(args.lambda_name)
    if not os.path.isfile('./' + args.lambda_name):
        d.unpack_lamdba(args.lambda_name)
    exit(0)


def list():
    global args
    d = DeployLambda(args.profile)
    d.list_lambdas()
    exit(0)


def unpack():
    global args
    d = DeployLambda(args.profile)
    d.unpack_lamdba(args.lambda_name)
    exit(0)