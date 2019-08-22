from troposphere import (
    ec2,
    GetAtt,
    Join, Ref)

from endpoints.sns_endpoint_security_group import sns_endpoint_security_group

from parameters import subnet_ids, vpc_id

sns_endpoint = ec2.VPCEndpoint(
    "SNSEndpoint",
    SecurityGroupIds=[GetAtt(sns_endpoint_security_group, "GroupId"), ],
    PrivatDnsEnbaled=True,
    ServiceName=Join("", ["com.amazonaws.", {"Ref": "AWS::Region"}, ".sns"]),
    SubnetIds=Ref(subnet_ids),
    VpcEndpointType="Interface",
    VpcId=vpc_id,
)
