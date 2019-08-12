import time
import uuid
import boto3
import logging

from config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def init_dynamo_db_table():
    try:
        dynamo_db = boto3.resource("dynamodb")
        table = dynamo_db.Table(Config.DYNAMO_DB_TABLE_NAME)
        return table
    except Exception as e:
        logger.error("ERROR: Failed to init DynamoDB")
        logger.error(e)
        return None


class LambdaExecutionStatuses(object):
    INITIALIZATION = "INITIALIZATION"
    FAILED_TO_INIT = "FAILED_TO_INIT"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"


def create_lambda_status_record(table, lambda_name, status):
    record_id = str(uuid.uuid4())

    now = int(time.time())
    data = {
        "lambda_name": lambda_name,
        "date_started": now,
        "execution_status": status,
        "uuid": record_id,
    }
    return table.put_item(Item=data), record_id


def update_record_status(table, status, lambda_name, record_id):
    response = table.update_item(
        Key={
            'lambda_name': lambda_name,
            'uuid': record_id,
        },
        UpdateExpression="set execution_status = :r",
        ExpressionAttributeValues={':r': status},
        ReturnValues="UPDATED_NEW"
    )
    return response
