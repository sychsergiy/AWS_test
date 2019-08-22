from troposphere import ec2, GetAtt

from main.resources.lambda_security_group import lambda_security_group

rds_security_group = ec2.SecurityGroup(
    "RDSSecurityGroup",
    GroupDescription="Ingress for RDS Instance",
    SecurityGroupIngress=[
        {
            "IpProtocol": "tcp",
            "FromPort": "5432",
            "ToPort": "5432",
            "SourceSecurityGroupId": GetAtt(lambda_security_group, "GroupId"),
        }
    ],
)
