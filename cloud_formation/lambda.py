import logging
import boto3

from config import Config

from services.sns import send_message_to_email_topic
from services.dynamodb import DynamoDBTable, LambdaExecutionStatuses
from services.rds import PostgresDB, connect_to_postgres

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
sns = boto3.resource("sns")


def handler(event, context):
    lambda_name = "aws_test"

    dynamo_db_table = DynamoDBTable(dynamodb.Table(Config.DYNAMO_DB_TABLE_NAME))

    _, record_id = dynamo_db_table.create_lambda_status_record(lambda_name, LambdaExecutionStatuses.INITIALIZATION)
    logger.info("DynamoDB record created")

    rds_connection = connect_to_postgres(Config)
    if not rds_connection:
        dynamo_db_table.update_record_status(LambdaExecutionStatuses.FAILED_TO_INIT, lambda_name, record_id)
        return "Failed to connect to RDS"

    db = PostgresDB(rds_connection)
    db.migrate()

    dynamo_db_table.update_record_status(LambdaExecutionStatuses.IN_PROGRESS, lambda_name, record_id)
    logger.info("DynamoDB record updated")

    # source_s3 = event['Records'][0]['s3']
    # source_bucket_name, updated_file_name = source_s3['bucket']['name'], source_s3['object']['key']
    source_bucket_name, updated_file_name = "test", "test"
    # todo: retrieve from event, now is not possible because of messaging thorough SNS instead of directly from S3

    db.insert_record(source_bucket_name, updated_file_name)
    logger.info("SQL query executed")

    sent_successfully = send_message_to_email_topic(sns, "Hello World")
    logger.info("Send email message executed")

    if sent_successfully:
        dynamo_db_table.update_record_status(
            LambdaExecutionStatuses.SUCCESS, lambda_name, record_id
        )
    else:
        dynamo_db_table.update_record_status(
            LambdaExecutionStatuses.FAILED, lambda_name, record_id
        )

    return "Success"
