from troposphere import ec2

lambda_security_group = ec2.SecurityGroup(
    "LambdaSecurityGroup", GroupDescription="SecurityGroup for LambdaHandler"
)
