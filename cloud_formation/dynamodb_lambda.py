from services.dynamodb import (
    init_dynamo_db_table,
    update_record_status,
    create_lambda_status_record,
    LambdaExecutionStatuses
)


def handler(event, context):
    lambda_name = "aws_test"
    dynamo_db_table = init_dynamo_db_table()
    if not dynamo_db_table:
        return "Failed to connect to DynamoDB"
    _, record_id = create_lambda_status_record(
        dynamo_db_table, lambda_name, LambdaExecutionStatuses.INITIALIZATION
    )

    update_record_status(
        dynamo_db_table, LambdaExecutionStatuses.IN_PROGRESS, lambda_name, record_id
    )

    source_s3 = event['Records'][0]['s3']
    source_bucket_name, updated_file_name = source_s3['bucket']['name'], source_s3['object']['key']

    update_record_status(
        dynamo_db_table, LambdaExecutionStatuses.SUCCESS, lambda_name, record_id
    )
    return "Inserted record with updated_file_name: %s" % updated_file_name
