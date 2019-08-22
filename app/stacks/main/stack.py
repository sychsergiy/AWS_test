from troposphere import Template

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
)
from stacks.main.outputs import (
    lambda_security_group_output
)


def template_factory(parameters, resources, outputs):
    t = Template()
    for param in parameters:
        t.add_parameter(param)
    for resource in resources:
        t.add_resource(resource)
    for output in outputs:
        t.add_output(output)
    return t


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
    ],
    [lambda_security_group_output, ]
)
