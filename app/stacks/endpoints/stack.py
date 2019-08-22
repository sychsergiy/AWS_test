from troposphere import Template

from stacks.endpoints.resources.sns_endpoint_security_group import sns_endpoint_security_group
from stacks.endpoints.resources.sns_endpoint import sns_endpoint
from stacks.endpoints.resources.dynamodb_endpoint import dynamodb_endpoint

from stacks.parameters import (
    route_tables_ids,
    vpc_id,
    subnet_ids,
)


def template_factory(parameters, resources):
    t = Template()
    for param in parameters:
        t.add_parameter(param)
    for resource in resources:
        t.add_resource(resource)
    return t


template = template_factory(
    [route_tables_ids, vpc_id, subnet_ids],
    [sns_endpoint, sns_endpoint_security_group, dynamodb_endpoint, ]
)
