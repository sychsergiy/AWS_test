from troposphere import awslambda, GetAtt, Ref

from main.resources.lambda_handler_role import lambda_handler_role
from main.resources.lambda_security_group import lambda_security_group
from main.resources.rds_instance import rds_instance

from parameters import (
    source_code_s3_bucket,
    source_code_s3_bucket_key,
    subnet_ids,
    rds_db_name,
    rds_master_password,
    rds_master_username,
)

lambda_handler = awslambda.Function(
    "LambdaHandler",
    Description="test lambda with access to RDS, SNS, DynamoDB. Will be triggered by SNS",
    Handler="lambda.handler",
    MemorySize=128,
    Code=awslambda.Code(
        S3Bucket=Ref(source_code_s3_bucket),
        S3Key=Ref(source_code_s3_bucket_key),
    ),
    Role=GetAtt(lambda_handler_role, "Arn"),
    Runtime="python2.7",
    Timeout=3,
    VpcConfig=awslambda.VPCConfig(
        SubnetIds=Ref(subnet_ids),
        SecurityGroupIds=[GetAtt(lambda_security_group, "GroupId")],
    ),
    Environment=awslambda.Environment(
        Variables={
            "DB_HOST": GetAtt(rds_instance, "Endpoint.Address"),
            "DB_PORT": GetAtt(rds_instance, "Endpoint.Port"),
            "DB_NAME": Ref(rds_db_name),
            "DB_USER": Ref(rds_master_username),
            "DB_PASSWORD": Ref(rds_master_password),
            "SNS_TOPIC_ARN": "not yet",  # todo: add after creating SNS topic for sending emails
            "DYNAMO_DB_TABLE_NAME": "not yet",  # todo: add after creating DynamoDB instance
        }
    ),
)
