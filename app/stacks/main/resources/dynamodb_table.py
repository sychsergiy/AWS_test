from troposphere import dynamodb

dynamodb_table = dynamodb.Table(
    "DynamoDBTable",
    AttributeDefinitions=[
        dynamodb.AttributeDefinition(AttributeName="uuid", AttributeType="S"),
        dynamodb.AttributeDefinition(
            AttributeName="lambda_name", AttributeType="S"
        ),
    ],
    KeySchema=[
        dynamodb.KeySchema(AttributeName="uuid", KeyType="HASH"),
        dynamodb.KeySchema(AttributeName="lambda_name", KeyType="RANGE"),
    ],
    ProvisionedThroughput=dynamodb.ProvisionedThroughput(
        ReadCapacityUnits=2, WriteCapacityUnits=2
    ),
)
