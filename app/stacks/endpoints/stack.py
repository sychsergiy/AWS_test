from stacks.endpoints.resources import (
    sns_endpoint_security_group,
    sns_endpoint,
    dynamodb_endpoint,
)

from stacks.parameters import route_tables_ids, vpc_id, subnet_ids

from stacks.util import template_factory

STACK_NAME = "Endpoints"

template = template_factory(
    [route_tables_ids, vpc_id, subnet_ids],
    [sns_endpoint, sns_endpoint_security_group, dynamodb_endpoint],
    [],
)
