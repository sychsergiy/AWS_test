from troposphere import (
    ec2,
)

rds_security_group = ec2.SecurityGroup(
    "RDSSecurityGroup",
    GroupDescription="Ingress for RDS Instance",
    SecurityGroupIngress=[
        ec2.SecurityGroupIngress(
            "RDSSecurityGroupIngress",
            IpProtocol="tcp",
            FromPort=5432,
            ToPort=5432,
            # todo: add lambda security group
            # SourceSecurityGroupId=GetAtt(lambda_handler_security_group, "GroupId")
        )
    ]
)
