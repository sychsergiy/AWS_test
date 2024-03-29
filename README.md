# AWS Task:
1. Create S3 bucket (enable versioning)
2. Create RDS database.
3. Create lambda function to process some info from a text file in bucket when new version of the file is uploaded (S3 event to invoke lambda) and put the info it into RDS table.
4. When lambda starts, put the info about running process into DynamoDB, when lambda finishes, update the info about the finished process.
5. Create SNS topic for lambda to push notification after finishing.
6. SNS should sent email to you.
7. Lambda should assume IAM role with all needed IAM policies to gain permissions for all the operations it performs.
- For all operations with AWS from within lambda use boto3 python library.
- Create all the infrastructure through Cloudformation. Use troposphere python library as a wrapper for Cloudformation.
- Use sceptre python library to store variables from troposphere. There should be 2 separate configs for dev and qa envs. 

## How to run?
To build lambda source code and push to S3 bucket:
1) `cd lambda_src`
2) `make push`

To generate stack templates from troposphere:
1) `cd app`
2) `python cli.py generate`

Or generate each stack template one by one:
- `python cli.py generate-main-stack-template`
- `python cli.py generate-emails-push-stack-template`
- `python cli.py generate-endpoints-stack-template`

To create stacks in CloudFormation (order is important):
1) `cd app`
1) `sceptre create dev/emails-push.yaml`
1) `sceptre create dev/main.yaml`
1) `sceptre create dev/endpoints.yaml`




