from troposphere import Template, Output

from endpoints.sns_endpoint_security_group import sns_endpoint_security_group
from endpoints.sns_endpoint import sns_endpoint
from endpoints.dynamodb_endpoint import dynamodb_endpoint

from parameters import (
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


t = template_factory(
    [route_tables_ids, vpc_id, subnet_ids],
    [sns_endpoint, sns_endpoint_security_group, dynamodb_endpoint, ]
)

with open("endpoints.yaml", "w") as f:
    f.write(t.to_yaml())
