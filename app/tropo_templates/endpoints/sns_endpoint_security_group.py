from troposphere import (
    ec2,
    GetAtt)

from resources.lambda_security_group import lambda_security_group

sns_endpoint_security_group = ec2.SecurityGroup(
    "SNSEndpointSecurityGroup",
    GroupDescription="SecurityGroup for SNS endpoint",
    SecurityGroupIngress=[
        {
            "IpProtocol": "tcp",
            "FromPort": 0,
            "ToPort": 65535,
            "SourceSecurityGroupId": GetAtt(lambda_security_group, "GroupId")
        }
    ]
)
