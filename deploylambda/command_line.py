#!/usr/bin/env python
import os
import argparse
from deploylambda import DeployLambda
parser = argparse.ArgumentParser(description='Deploy some lambdas')

parser.add_argument('--profile', help='specify an aws profile to use, if not the default', default='default')
parser.add_argument('lambda_name', nargs='?', help='lambda name')
parser.add_argument('alias_name', nargs='?', help='alias')
args = parser.parse_args()


def deploy_lambda():
    d = DeployLambda(args.profile, args.lambda_name)
    d.backup_old_lambda(os.getcwd())
    zip = DeployLambda.create_zip(args.lambda_name, os.getcwd())
    d.deploy_new_lambda(zip)


def update():
    d = DeployLambda(args.profile, args.lambda_name)
    zip = DeployLambda.create_zip(args.lambda_name, os.getcwd())
    d.deploy_new_lambda(zip)


def package_lambda():
    DeployLambda.create_zip(args.lambda_name, os.getcwd())


def backup_lambda():
    d = DeployLambda(args.profile, args.lambda_name)
    d.backup_old_lambda(os.getcwd())
    if not os.path.isfile('./' + args.lambda_name):
        DeployLambda.unpack_lamdba(args.lambda_name, os.getcwd())


def list_lambda():
    d = DeployLambda(args.profile)
    d.list_lambdas()


def unpack_lambda():
    DeployLambda.unpack_lamdba(args.lambda_name, os.getcwd())


def metadata_lambda():
    d = DeployLambda(args.profile, args.lambda_name)
    d.update_metadata(os.getcwd())


def alias_lambda():
    d = DeployLambda(args.profile, args.lambda_name)
    d.version_and_create_alias(args.alias_name)


def promote_lambda():
    d = DeployLambda(args.profile, args.lambda_name)
    d.promote_alias('stage', args.alias_name)