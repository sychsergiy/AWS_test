from endpoints.resources.dynamodb_endpoint import dynamodb_endpoint
from endpoints.resources.sns_endpoint import sns_endpoint
from endpoints.resources.sns_endpoint_security_group import sns_endpoint_security_group

__all__ = [
    dynamodb_endpoint,
    sns_endpoint,
    sns_endpoint_security_group,
]
