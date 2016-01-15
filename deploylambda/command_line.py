#!/usr/bin/env python
import deploylambda
import os
import subprocess
import sys
import ConfigParser


def main():

    if not os.path.isfile(os.path.expanduser('~') +'/.aws/credentials'):
        print 'please run aws configure, missing credentials'
        exit(1)

    profile = 'default'

    userconfig = ConfigParser.ConfigParser()
    userconfig.readfp(open(os.path.expanduser('~') +'/.aws/credentials'))

    os.environ['AWS_ACCESS_KEY_ID'] = userconfig.get(profile, 'aws_access_key_id')
    os.environ['AWS_SECRET_ACCESS_KEY'] = userconfig.get(profile, 'aws_secret_access_key')

    if not os.path.isfile(os.path.expanduser('~') +'/.aws/credentials'):
        print 'please run aws configure, missing config'
        exit(1)

    regionconfig = ConfigParser.ConfigParser()
    regionconfig.readfp(open(os.path.expanduser('~') +'/.aws/config'))
    os.environ['AWS_DEFAULT_REGION'] = regionconfig.get(profile, 'region')

    deploylambda.get_account()
    try:
        subprocess.check_output("command -v aws", shell=True)
    except:
        print 'error: install aws cli tools'
        exit(1)

    try:
        sys.argv[1]
    except:
        deploylambda.print_lambdas()
        exit(1)


    lambda_name = sys.argv[1]
    print "Deploy lambda "+lambda_name
    deploylambda.backup_old_lambda(lambda_name)
    zipname = deploylambda.create_zip(lambda_name)
    deploylambda.deploy_new_lambda(lambda_name)
    exit(0)


