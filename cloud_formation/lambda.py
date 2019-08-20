import logging

from services.dynamodb import (
    init_dynamo_db_table,
    create_lambda_status_record,
    update_record_status,
    LambdaExecutionStatuses,
)
from services.rds import init_rds, insert_record_to_rds
from services.sns import send_message_to_email_topic

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    lambda_name = "aws_test"
    dynamo_db_table = init_dynamo_db_table()
    logger.info("started")
    if not dynamo_db_table:
        return "Failed to connect to DynamoDB"
    _, record_id = create_lambda_status_record(
        dynamo_db_table, lambda_name, LambdaExecutionStatuses.INITIALIZATION
    )
    logger.info("DynamoDB record created")

    rds_connection = init_rds()
    if not rds_connection:
        create_lambda_status_record(dynamo_db_table, lambda_name, LambdaExecutionStatuses.FAILED_TO_INIT)
        return "Failed to connect to RDS"

    update_record_status(
        dynamo_db_table, LambdaExecutionStatuses.IN_PROGRESS, lambda_name, record_id
    )
    logger.info("DynamoDB record updated")

    source_s3 = event['Records'][0]['s3']
    source_bucket_name, updated_file_name = source_s3['bucket']['name'], source_s3['object']['key']

    with rds_connection.cursor() as cursor:
        insert_record_to_rds(cursor, source_bucket_name, updated_file_name)
        rds_connection.commit()

    logger.info("SQL query executed")
    sent_successfully = send_message_to_email_topic("Hello World")
    logger.info("Send email message executed")
    if sent_successfully:
        update_record_status(
            dynamo_db_table, LambdaExecutionStatuses.SUCCESS, lambda_name, record_id
        )
    else:
        update_record_status(
            dynamo_db_table, LambdaExecutionStatuses.FAILED, lambda_name, record_id
        )

    return "Inserted record with updated_file_name: %s" % updated_file_name
