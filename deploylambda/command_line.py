#!/usr/bin/env python
import os
import argparse
from deploylambda import DeployLambda
parser = argparse.ArgumentParser(description='Deploy some lambdas')
parser.add_argument('--profile', help='specify an aws profile to use, if not the default', default='default')


def deploy_lambda():
    parser.add_argument('lambda_name', help='lambda name')
    args = parser.parse_args()
    d = DeployLambda(args.profile, args.lambda_name)
    d.backup_old_lambda(os.getcwd())
    zip = DeployLambda.create_zip(args.lambda_name, os.getcwd())
    d.deploy_new_lambda(zip)


def update():
    parser.add_argument('lambda_name', help='lambda name')
    args = parser.parse_args()
    d = DeployLambda(args.profile, args.lambda_name)
    zip = DeployLambda.create_zip(args.lambda_name, os.getcwd())
    d.deploy_new_lambda(zip)


def package_lambda():
    parser.add_argument('lambda_name', help='lambda name')
    args = parser.parse_args()
    zip = DeployLambda.create_zip(args.lambda_name, os.getcwd())
    print('created ' + zip)


def package_venv_lambda():
    parser.add_argument('lambda_name', help='lambda name')
    parser.add_argument('--extra', help='extra module folder [aws compiled modules like psycopg2], by relative path', default='')
    args = parser.parse_args()
    zip = DeployLambda.create_venv_zip(args.lambda_name, os.getcwd(), args.extra)
    print('created ' + zip)


def backup_lambda():
    parser.add_argument('lambda_name', help='lambda name')
    args = parser.parse_args()
    d = DeployLambda(args.profile, args.lambda_name)
    d.backup_old_lambda(os.getcwd())
    if not os.path.isfile('./' + args.lambda_name):
        DeployLambda.unpack_lamdba(args.lambda_name, os.getcwd())


def list_lambda():
    args = parser.parse_args()
    d = DeployLambda(args.profile)
    d.list_lambdas()


def unpack_lambda():
    parser.add_argument('lambda_name', help='lambda name')
    args = parser.parse_args()
    DeployLambda.unpack_lamdba(args.lambda_name, os.getcwd())


def metadata_lambda():
    parser.add_argument('lambda_name', help='lambda name')
    args = parser.parse_args()
    d = DeployLambda(args.profile, args.lambda_name)
    d.update_metadata(os.getcwd())


def alias_lambda():
    parser.add_argument('lambda_name', help='lambda name')
    parser.add_argument('alias_name', help='alias')
    args = parser.parse_args()
    d = DeployLambda(args.profile, args.lambda_name)
    d.version_and_create_alias(args.alias_name)


def promote_lambda():
    parser.add_argument('lambda_name', help='lambda name')
    parser.add_argument('alias_name', help='alias')
    args = parser.parse_args()
    d = DeployLambda(args.profile, args.lambda_name)
    d.promote_alias('stage', args.alias_name)