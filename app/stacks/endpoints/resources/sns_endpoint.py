from troposphere import (
    ec2,
    GetAtt,
    Join, Ref)

from stacks.endpoints.resources.sns_endpoint_security_group import sns_endpoint_security_group

from stacks.parameters import subnet_ids, vpc_id

sns_endpoint = ec2.VPCEndpoint(
    "SNSEndpoint",
    SecurityGroupIds=[GetAtt(sns_endpoint_security_group, "GroupId"), ],
    PrivateDnsEnabled=True,
    ServiceName=Join("", ["com.amazonaws.", {"Ref": "AWS::Region"}, ".sns"]),
    SubnetIds=Ref(subnet_ids),
    VpcEndpointType="Interface",
    VpcId=Ref(vpc_id),
)
