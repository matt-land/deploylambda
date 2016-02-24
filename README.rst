AWS Python Lambda Deploy Module
=========================


Deploy-lambda is a command line tool for maintance of aws python lambda functions. It can backup the current version of a lambda, create a new deployment package, and push it out to an aws account. 

You can hook up to existing AWS python lambda functions, no special magic required.


Installation
-----------------

>>> `python setup.py build`

>>> `(sudo) python setup.py install`

Optionally: install the AWS Cli toolkit if not already installed

http://docs.aws.amazon.com/cli/latest/userguide/installing.html

>>> `pip install awscli`


@todo add pip support


Setup
------------------

aws cli must be configured with your account credentials by running `aws configure`

The tool supports multiple aws accounts, choose them with the parameter --profile <profile name>

Example
>>> `list-lambda --profile sandbox` <- uses a non-default AWS profile.

Look at ~/.aws/credentials for available profiles


Usage
------------------

>>> `list-lambda` <-- list current lambda functions in th default account

>>> `deploy-lambda my-lambda-name` <-- backup, package, and deploy the newest local lambda function

>>> `update-lambda my-lambda-name` <-- deploy the newest local lambda function (no backups)

>>> `backup-lambda my-lambda-name` <-- create a local backup of the current remote lambda function

>>> `package-lambda my-lambda-name` <-- build a deployment package (zip) of the newest local lambda function



call 'deploy-lambda' from the command line, one folder level above the source code

example:

/my-lambda-function <----- one level below me

`deploy-lambda my-lambda-function`


Recipes
_________________

To start using with exiting lambda functions
`list-lambda`
`backup-lambda myawslambda`
... make changes to the code
`deploy-lambda myawslambda`


Notes
------------------
lambda function name must match the folder name (exactly)