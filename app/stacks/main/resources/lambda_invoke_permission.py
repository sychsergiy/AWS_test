from troposphere import awslambda, Ref, GetAtt
from stacks.main.resources.lambda_handler import lambda_handler
from stacks.main.resources.bucket_updates_topic import bucket_updates_topic

lambda_invoke_permission = awslambda.Permission(
    "LambdaHandlerInvokePermission",
    Action="lambda:InvokeFunction",
    Principal="sns.amazonaws.com",
    SourceArn=Ref(bucket_updates_topic),
    FunctionName=GetAtt(lambda_handler, "Arn"),
)
