import json
import zipfile
import shutil
import wget
import os
import subprocess
import ConfigParser

def get_account():
    account = subprocess.check_output('aws iam list-account-aliases', shell=True)
    obj = json.loads(account)
    try :
        return obj['AccountAliases'][0]
    except:
        return 'account'


def create_zip(lambda_name):
    zipname = lambda_name + '.zip'
    print "Creating deployment package "+zipname
    subpath = "./" + lambda_name
    if not os.path.isdir(subpath):
        raise NameError('lambda source code folder not found '+lambda_name)
    lastpath = os.getcwd()
    os.chdir(subpath)

    if os.path.isfile(zipname):
        os.unlink(zipname)
    zf = zipfile.ZipFile(zipname, mode='w', compression=zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == '.DS_Store':
                continue
            if file == zipname:
                continue
            zf.write(root+"/"+file)
    zf.close()
    if os.path.isfile(lastpath + "/"+zipname):
        os.unlink(lastpath+"/"+zipname)
    shutil.move(zipname, lastpath)
    os.chdir(lastpath)
    return zipname


def backup_old_lambda(lambda_name):
    name = lambda_name + "-last.zip"
    print "Backing up existing lambda as "+name
    if os.path.isfile(name):
        os.unlink(name)
    jsonstring = subprocess.check_output("aws lambda get-function --function-name " + lambda_name, shell=True)
    obj = json.loads(jsonstring)
    wget.download(obj['Code']['Location'], name)
    print ''

def unpack_lamdba(lamdba_name):
    print "Unpacking lambda to local file system as "+lamdba_name
    zipname = lamdba_name + "-last.zip"
    pathname = "./" + lamdba_name
    if not os.path.isfile(zipname):
        raise NameError('missing zip file to unpack '+ zipname)
    if os.path.isfile(pathname):
        raise NameError('lambda function code already exists in '+ pathname)
    zf = zipfile.ZipFile(zipname, 'r')
    zf.extractall(pathname)


def print_lambdas():
    print "Available lambda functions in "+get_account()
    response = subprocess.check_output("aws lambda list-functions", shell=True)
    obj = json.loads(response)
    for function in obj['Functions']:
        print "-> "+function['FunctionName']
    print "Call again with a lambda name as an argument"


def deploy_new_lambda(lambda_name):
    print "Deploying lambda [" + lambda_name + "] in "+ get_account()
    code = "aws lambda update-function-code --function-name " + lambda_name + " --zip-file fileb://" + lambda_name + ".zip"
    #print code
    output = subprocess.check_output(code, shell=True)
    obj = json.loads(output)
    print " Last Modified: "+obj['LastModified']
    print " Sha: "+obj['CodeSha256']
    print " Code Size: "+str(obj['CodeSize'])
    #print "https://console.aws.amazon.com/lambda/home?region="+regionconfig.get(profile, 'region')+"#/functions/"+lambda_name+"?tab=code"


def setupOS():
    try:
        subprocess.check_output("command -v aws", shell=True)
    except:
        print 'error: install aws cli tools'
        exit(1)

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

