from troposphere import Output, Export, GetAtt

from stacks.main.resources import lambda_security_group

STACK_NAME = "Main"

lambda_security_group_id_output_name = "LambdaSecurityGroupId"
lambda_security_group_id_export_name = "{}-{}".format(
    STACK_NAME, lambda_security_group_id_output_name
)
lambda_security_group_output = Output(
    lambda_security_group_id_output_name,
    Value=GetAtt(lambda_security_group, "GroupId"),
    Export=Export(lambda_security_group_id_export_name),
)
