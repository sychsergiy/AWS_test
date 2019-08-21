from troposphere import (
    Parameter
)

source_code_s3_bucket = Parameter(
    "SourceCodeS3Bucket",
    Description="Bucket with source code",
    Type="String",
    Default="aws.cloudformation.test",
)

source_code_s3_bucket_key = Parameter(
    "SourceCodeS3BucketKey",
    Description="Path to file with lambda deployment package",
    Type="String",
    Default="function.zip"  # todo: add environment prefix
)

lambda_handler_function_name = Parameter(
    "LambdaHandlerFunctionName",
    Description="Bucket with source code",
    Type="String",
    Default="LambdaHandler",  # todo: add environment prefix
)
