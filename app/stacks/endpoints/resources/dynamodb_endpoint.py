from troposphere import ec2, Join, Ref

from stacks.parameters import route_tables_ids, vpc_id

dynamodb_endpoint = ec2.VPCEndpoint(
    "DynamoDBEndpoint",
    ServiceName=Join(
        "", ["com.amazonaws.", {"Ref": "AWS::Region"}, ".dynamodb"]
    ),
    RouteTableIds=Ref(route_tables_ids),
    VpcEndpointType="Gateway",
    VpcId=Ref(vpc_id),
)
