from stacks.parameters import (
    subnet_ids,
    rds_master_password,
    rds_master_username,
    rds_db_name,
    lambda_handler_function_name,
    source_code_s3_bucket_key,
    source_code_s3_bucket,
)
from stacks.main.resources import (
    bucket_updates_topic_policy,
    bucket_updates_topic,
    lambda_handler,
    lambda_invoke_permission,
    lambda_handler_role,
    lambda_security_group,
    rds_instance,
    rds_security_group,
    rds_subnet_group,
    s3_bucket,
    dynamodb_table,
)
from stacks.main.outputs import lambda_security_group_output

from stacks.util import template_factory

template = template_factory(
    [
        subnet_ids,
        rds_db_name,
        rds_master_username,
        rds_master_password,
        lambda_handler_function_name,
        source_code_s3_bucket,
        source_code_s3_bucket_key,
    ],
    [
        bucket_updates_topic_policy,
        bucket_updates_topic,
        lambda_handler,
        lambda_invoke_permission,
        lambda_handler_role,
        lambda_security_group,
        rds_instance,
        rds_security_group,
        rds_subnet_group,
        s3_bucket,
        dynamodb_table,
    ],
    [lambda_security_group_output],
)
