from troposphere import (
    Output,
    Export,
    Ref
)

from constants import MAIN_STACK_NAME
from resources import lambda_security_group

output_name = "LambdaSecurityGroup"

lambda_security_group_output = Output(
    output_name,
    Value=Ref(lambda_security_group),
    Export=Export('{}-{}'.format(MAIN_STACK_NAME, output_name))
)
