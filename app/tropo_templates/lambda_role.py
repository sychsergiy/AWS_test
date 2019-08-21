from troposphere import (
    iam
)

lambda_handler_role = iam.Role(
    "LambdaHandlerRole",
    Path="/",
    Policies=[
        iam.Policy(
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
        ),
        iam.Policy(
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
                                "DynamoDBTable",
                                "Arn"
                            ]
                        }
                    }
                ]
            }
        ),
        iam.Policy(
            PolicyName="SNSPublish",
            PolicyDocument={
                "Statement": [
                    {
                        "Action": [
                            "sns:Publish"
                        ],
                        "Resource": [
                            {
                                "Ref": "EmailsSNSTopic"
                            }
                        ],
                        "Effect": "Allow"
                    }
                ]
            }
        )
    ],
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

from pprint import pprint
pprint(lambda_handler_role.to_dict())
