from troposphere import (
    iam
)

sns_publish_policy = iam.Policy(
    PolicyName="SNSPublish",
    PolicyDocument={
        "Statement": [
            {
                "Action": [
                    "sns:Publish"
                ],
                "Resource": [
                    {
                        "Ref": "EmailsSNSTopic"  # todo: change on tropo object
                    }
                ],
                "Effect": "Allow"
            }
        ]
    }
)

dynamodb_read_write_policy = iam.Policy(
    PolicyName="DynamoDbReadWritePolicy",
    PolicyDocument={
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:BatchGetItem",
                    "dynamodb:BatchWriteItem",
                    "dynamodb:PutItem",
                    "dynamodb:DeleteItem",
                    "dynamodb:GetItem",
                    "dynamodb:UpdateItem"
                ],
                "Resource": {
                    "Fn::GetAtt": [
                        "DynamoDBTable",  # todo: change on tropo object
                        "Arn"
                    ]
                }
            }
        ]
    }
)

cloud_watch_logs_policy = iam.Policy(
    PolicyName="CloudwatchLogs",
    PolicyDocument={
        "Statement": [
            {
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:GetLogEvents",
                    "logs:PutLogEvents"
                ],
                "Resource": [
                    "arn:aws:logs:*:*:*"
                ],
                "Effect": "Allow"
            }
        ]
    }
)

lambda_handler_role = iam.Role(
    "LambdaHandlerRole",
    Path="/",
    Policies=[cloud_watch_logs_policy],  # todo: add other policies
    AssumeRolePolicyDocument={
        "Statement": [
            {
                "Action": [
                    "sts:AssumeRole"
                ],
                "Effect": "Allow",
                "Principal": {
                    "Service": [
                        "lambda.amazonaws.com"
                    ]
                }
            }
        ]
    },
    ManagedPolicyArns=[
        "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
    ]
)
