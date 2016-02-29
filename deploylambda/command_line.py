#!/usr/bin/env python
import os
import argparse
from deploylambda import DeployLambda
parser = argparse.ArgumentParser(description='Deploy some lambdas')

parser.add_argument('--profile', help='specify an aws profile to use, if not the default', default='default')
parser.add_argument('lambda_name', nargs='?', help='lambda name')
parser.add_argument('alias_name', nargs='?', help='alias')
args = parser.parse_args()


def deploy():
    global args
    d = DeployLambda(args.profile, args.lambda_name)
    d.backup_old_lambda()
    zip = DeployLambda.create_zip(args.lambda_name)
    d.deploy_new_lambda(zip)
    exit(0)


def update():
    global args
    d = DeployLambda(args.profile, args.lambda_name)
    zip = DeployLambda.create_zip(args.lambda_name)
    d.deploy_new_lambda(zip)
    exit(0)


def package():
    global args
    DeployLambda.create_zip(args.lambda_name)
    exit(0)


def backup():
    global args
    d = DeployLambda(args.profile, args.lambda_name)
    d.backup_old_lambda()
    if not os.path.isfile('./' + args.lambda_name):
        DeployLambda.unpack_lamdba(args.lambda_name)
    exit(0)


def list():
    global args
    d = DeployLambda(args.profile)
    d.list_lambdas()
    exit(0)


def unpack():
    global args
    DeployLambda.unpack_lamdba(args.lambda_name)
    exit(0)


def metadata():
    global args
    d = DeployLambda(args.profile, args.lambda_name)
    d.update_metadata()


def alias():
    global args
    d = DeployLambda(args.profile, args.lambda_name)
    d.version_and_create_alias(args.alias_name)


def promote():
    global args
    d = DeployLambda(args.profile, args.lambda_name)
    d.promote_alias('stage', args.alias_name)