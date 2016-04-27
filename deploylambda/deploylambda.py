import json
import zipfile
import wget
import os
import subprocess
import ConfigParser
import sys

class DeployLambda:

    profile = ''
    function_name = ''

    def __init__(self, profile='default', function_name=''):
        self.profile = profile
        self.function_name = function_name
        self._setup_os()

    def get_account(self):
        """get the alias from the account we are using"""
        try:
            account = subprocess.check_output('aws iam list-account-aliases --profile ' + self.profile, shell=True)
            obj = json.loads(account)
            return obj['AccountAliases'][0]
        except:
            return '[unknown account]'

    @staticmethod
    def create_venv_zip(function_name, path, extrapath=''):
        if not path.endswith('/'):
            path = path + '/'
        extrapaths = ['venv/lib/python2.7/site-packages', 'venv/src']
        if extrapath and extrapath is not '.':
            extrapaths.append(extrapath)
        function_name = function_name.replace('.py', '', 1)
        zippath = path + "../" + function_name + '.zip'
        if os.path.isfile(zippath):
            os.unlink(zippath)
        counter = 0
        os.chdir(path)
        zf = zipfile.ZipFile(zippath, mode='w', compression=zipfile.ZIP_DEFLATED)

        if not os.path.isfile(function_name + '.py'):
            raise Exception('no such file ' + path + function_name + '.py')
        zf.write(function_name + '.py')
        if os.path.isfile(function_name + '-config.json'): #add config if we have it
            zf.write(function_name + '-config.json')

        for subpath in extrapaths:
            os.chdir(path + subpath)
            for root, dirs, files in os.walk('.', topdown=True):
                if '.git' in dirs:
                    dirs.remove('.git')

                for file in files:
                    if root.startswith('./boto'): #for free on aws
                        continue
                    if  root.startswith('./psycopg2') and 'aws' not in subpath: #psycopg2 from aws folder
                        continue
                    if file == '.DS_Store':
                        continue
                    if file.endswith('.zip'): #skip zips
                        continue
                    if file.endswith(".pyc"):
                        continue
                    zf.write(root + "/" + file)
                    counter += 1
        zf.close()
        print str(counter) + " files added to "+ zippath
        return zippath

    @staticmethod
    def create_zip(function_name, path):
        zippath = path + "/../" + function_name + '.zip'
        counter = 0
        if os.path.isfile(zippath):
            os.unlink(zippath)
        zf = zipfile.ZipFile(zippath, mode='w', compression=zipfile.ZIP_DEFLATED)
        os.chdir(path)
        for root, dirs, files in os.walk('.', topdown=True):
            if '.git' in dirs:
                dirs.remove('.git')
            if 'test' in dirs:
                dirs.remove('test')
            for file in files:
                if file == '.DS_Store':
                    continue
                if file.endswith('.zip'): #skip zips
                    continue
                if file.endswith(".pyc"): #skip compiled
                    continue
                zf.write(root + "/" + file)
                counter += 1
        zf.close()
        #print str(counter) + " files added to "+ zippath
        return zippath

    def backup_old_lambda(self, path):
        name = path + '/../' + self.function_name + "-last.zip"
        print "Backing up existing lambda as " + name
        if os.path.isfile(name):
            os.unlink(name)
        try:
            json_string = subprocess.check_output("aws lambda get-function --function-name " + self.function_name + " --profile " + self.profile, shell=True)
            obj = json.loads(json_string)
            wget.download(obj['Code']['Location'], name)
            print ''
        except:
            raise Exception( "unable to back up old lambda " + str(sys.exc_info()))


    @staticmethod
    def unpack_lamdba(function_name, path):
        print "Unpacking lambda to local file system as " + function_name
        zipname = function_name + "-last.zip"
        pathname = path + "/../"
        if not os.path.isfile(zipname):
            raise NameError('missing zip file to unpack ' + zipname)
        if os.path.isfile(pathname):
            raise NameError('lambda function code already exists in ' + pathname)
        zf = zipfile.ZipFile(zipname, 'r')
        zf.extractall(pathname)

    def list_lambdas(self):
        print "Lambda functions in  [ " + self.get_account() + " ]"
        command = "aws lambda list-functions --profile " + self.profile
        try:
            response = subprocess.check_output(command, shell=True)
            obj = json.loads(response)
            for function in obj['Functions']:
                print " [ " + function['FunctionName'] + " ]"
                self.function_name = function['FunctionName']
                aliases = self._list_aliases()
                for alias in aliases:
                    print "   - [" + alias['Name'] + "] -> v" + alias['FunctionVersion']
        except:
            raise Exception("unable to list lambdas from [" + self.get_account() + "] using " + command + " " + str(sys.exc_info()))

    def deploy_new_lambda(self, zippath):
        print "Deploying lambda [ " + self.function_name + " ] in [ " + self.get_account() + " ]"
        try:
            code = "aws lambda update-function-code --function-name " + self.function_name + " --zip-file fileb://" + zippath + " --profile " + self.profile
            #print code
            output = subprocess.check_output(code, shell=True)
            obj = json.loads(output)
            #print " Last Modified: "+obj['LastModified']
            print " Sha: "+obj['CodeSha256']
            #print " Code Size: " + str(obj['CodeSize'])
        except Exception, e:
            raise Exception("unable to deploy lambdas from [" + self.get_account()+']')

    def _setup_os(self):
        try:
            subprocess.check_output("command -v aws", shell=True)
        except Exception, e:
            raise Exception( 'error: install aws cli tools')

        if not os.path.isfile(os.path.expanduser('~') + '/.aws/credentials'):
            raise Exception('please run aws configure, missing credentials')


        userconfig = ConfigParser.ConfigParser()
        userconfig.readfp(open(os.path.expanduser('~') + '/.aws/credentials'))
        os.environ['AWS_ACCESS_KEY_ID'] = userconfig.get(self.profile, 'aws_access_key_id')
        os.environ['AWS_SECRET_ACCESS_KEY'] = userconfig.get(self.profile, 'aws_secret_access_key')

        if not os.path.isfile(os.path.expanduser('~') + '/.aws/credentials'):
            raise Exception( 'please run aws configure, missing config')

        if self.profile != 'default':
            profile = 'profile ' + self.profile
        else:
            profile = self.profile
        regionconfig = ConfigParser.ConfigParser()
        regionconfig.readfp(open(os.path.expanduser('~') + '/.aws/config'))
        os.environ['AWS_DEFAULT_REGION'] = regionconfig.get(profile, 'region')

    def update_metadata(self, path):
        """get the current config"""
        try:
            code = "aws lambda get-function-configuration --function " + self.function_name + " --profile " + self.profile
            rawdata = subprocess.check_output(code, shell=True)
        except:
            raise Exception("unable to get lambda metadata " + str(sys.exc_info()))
        # get skeleton
        try:
            code = "aws lambda update-function-configuration --generate-cli-skeleton --profile " + self.profile
            data = subprocess.check_output(code, shell=True)
            skeleton = json.loads(data)
        except:
            raise Exception("unable to get skeleton config " + str(sys.exc_info()))

        # load our live data into a json we can compare with
        filename = self.function_name + '-config.json'
        live_obj = json.loads(rawdata)
        live_lambda_json = {}
        for key, value in skeleton.iteritems():
            if key in live_obj.keys():
                live_lambda_json[key] = live_obj[key]

        # store on disk if this is first call
        config_file = path + '/' + self.function_name + '-config.json'
        if not os.path.isfile(config_file):
            with open(filename, 'w') as f:
                f.write(json.dumps(live_lambda_json, indent=4))
                print "backed up metadata as " + filename
                return

        # check our file is valid json
        try:
            with open(filename) as json_file:
                file_obj = json.load(json_file)
        except:
            raise Exception("invalid json file detected " + filename)

        # build our input data from file
        cli_input_json = dict(skeleton.items() + file_obj.items())
        #pop this key if seen
        if 'VpcId' in cli_input_json['VpcConfig']:
            cli_input_json['VpcConfig'].pop('VpcId')


        # compare input file to live file config
        if json.dumps(live_lambda_json) == json.dumps(cli_input_json):
            #print "No metadata changes detected"
            return

        #print "updating metadata"
        try:
            code = "aws lambda update-function-configuration --function " + self.function_name + " --profile " + self.profile + " --cli-input-json " + json.dumps(json.dumps(cli_input_json))
            data = subprocess.check_output(code, shell=True)
        except:
            raise Exception("unable to update lambda metadata " + str(sys.exc_info()))

    def version_and_create_alias(self, name):
        """publish a version from $LATEST and add an alias"""
        version = self._create_version()
        #see if we need to create or update the alias

        aliases = self._list_aliases()
        hasAlias = False
        for alias in aliases:
            if alias['Name'] == name:
                hasAlias = True
                break
        if hasAlias:
            self._update_alias(name, version)
        else:
            self._create_alias(name, version)

    def promote_alias(self, promoted_name, existing_name):
        """for promoting lambdas between environments, like dev, stage, prod"""
        found_promoted_tag = False
        found_existing_tag = False
        aliases = self._list_aliases()
        for alias in aliases:
            if alias['Name'] == promoted_name:
                found_promoted_tag = True
            if alias['Name'] == existing_name:
                found_existing_tag = True
                version = alias['FunctionVersion']
            if found_existing_tag and found_promoted_tag:
                break
        if not found_existing_tag:
            raise Exception("can not find exiting alias " + existing_name)

        if not found_promoted_tag:
            self._create_alias(promoted_name, version)
        else:
            self._update_alias(promoted_name, version)

    def _create_version(self):
        try:
            code = "aws lambda publish-version --function-name " + self.function_name + " --profile " + self.profile
            data = subprocess.check_output(code, shell=True)
        except:
            raise Exception("unable to publish lambda version " + str(sys.exc_info()))

        response = json.loads(data)
        return response['Version']

    def _create_alias(self, name, version):
        try:
            code = "aws lambda create-alias --function-version " + version + " --function-name " + self.function_name + " --name " + name + " --profile " + self.profile
            data = subprocess.check_output(code, shell=True)
        except:
            raise Exception("unable to create alias to published version " + str(sys.exc_info()))
        response = json.loads(data)
        print "Created [ " + response['Name'] + " ] pointing to [ v" + version + " ] of [ " + self.function_name + " ]"
        return response

    def _update_alias(self, name, version):
        try:
            code = "aws lambda update-alias --function-version " + version + " --function-name " + self.function_name + " --name " + name + " --profile " + self.profile
            data = subprocess.check_output(code, shell=True)
        except:
            raise Exception("unable to create alias to published version " + str(sys.exc_info()))

        response = json.loads(data)
        print "Updated [ " + response['Name'] + " ] pointing to [ v" + version + " ] of [ " + self.function_name + " ]"
        return response

    def _list_aliases(self):
        try:
            code = "aws lambda list-aliases --function-name " + self.function_name + " --profile " + self.profile
            data = subprocess.check_output(code, shell=True)
        except:
            raise Exception("failed to list aliases for function " + str(sys.exc_info()))
        data = json.loads(data)
        return data['Aliases']


