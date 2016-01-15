AWS Python Lambda Deploy Module
=========================


This will backup the current version of your lambda, create a new package, and deploy it.


installation
-----------------


python setup.py build 
(sudo) python setup.py install



usage
------------------

`deploy-lambda` <-- list current lamda functions in th default account

`deploy-lambda my-lambda-name` <-- deploy the new lambda code


call 'deploy-lambda' from the command line, one folder level above the source code

example:

/my-lambda-function <----- one level below me

`deploy-lambda my-lambda-function`


requires
------------------

aws cli toolkit

http://docs.aws.amazon.com/cli/latest/userguide/installing.html

`pip install awscli`


setup
------------------

aws cli must be configured with your account credentials

`aws configure`

notes
------------------
lambda function name must match the folder name (exactly)