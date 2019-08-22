from troposphere import (
    Output,
    Export,
    Ref
)

from constants import MAIN_STACK_NAME
from main.resources import lambda_security_group

lambda_security_group_output_name = "LambdaSecurityGroup"
lambda_security_group_export_name = '{}-{}'.format(MAIN_STACK_NAME, lambda_security_group_output_name)
lambda_security_group_output = Output(
    lambda_security_group_output_name,
    Value=Ref(lambda_security_group),
    Export=Export(lambda_security_group_export_name)
)
