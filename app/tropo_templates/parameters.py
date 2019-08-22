from troposphere import Parameter

# General params
subnet_ids = Parameter(
    "SubnetIds",
    Description="Subnet for RDS and Lambda",
    Type="List<AWS::EC2::Subnet::Id>",
    Default="subnet-23e73349,subnet-568e8d2b,subnet-c8e7f185",
)
vpc_id = Parameter(
    "VPCId",
    Description="VPC id",
    Type="String",
    Default="vpc-5cbd5136",
)

route_tables_ids = Parameter(
    "RouteTablesIds",
    Description="Route tables ids for DynamoDB endpoint",
    Type="List<AWS::EC2::RouteTable>",
    Deafult="rtb-32640258",
)

# LambdaHandler Params
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
    Default="function.zip",  # todo: add environment prefix
)

lambda_handler_function_name = Parameter(
    "LambdaHandlerFunctionName",
    Description="Bucket with source code",
    Type="String",
    Default="LambdaHandler",  # todo: add environment prefix
)

# RDS params
rds_db_name = Parameter(
    "RDSDBName",
    Description="Name of database in create RDS instance",
    Type="String",
    Default="aws_training",
)

rds_master_username = Parameter(
    "RDSMasterUsername",
    Description="Root username",
    Type="String",
    Default="root",
)

rds_master_password = Parameter(
    "RDSMasterPassword",
    Description="Root password",
    Type="String",
    Default="rootroot",
)
