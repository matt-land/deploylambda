import json
import zipfile
import shutil
import wget
import os
import subprocess


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
    subpath = "../" + lambda_name
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
            #print root+"/"+file
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

