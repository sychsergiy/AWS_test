from troposphere import ec2

from stacks.endpoints.import_values import sns_topic_source_security_group_id

sns_endpoint_security_group = ec2.SecurityGroup(
    "SNSEndpointSecurityGroup",
    GroupDescription="SecurityGroup for SNS endpoint",
    SecurityGroupIngress=[
        {
            "IpProtocol": "tcp",
            "FromPort": 0,
            "ToPort": 65535,
            "SourceSecurityGroupId": sns_topic_source_security_group_id,
        }
    ],
)
