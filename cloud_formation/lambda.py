import time
import uuid
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_env_var(var_name, required=True):
    value = os.environ.get(var_name)
    if required:
        if not value:
            raise Exception("Env var: {} is required".format(var_name))
    return value


class Config(object):
    DYNAMO_DB_TABLE_NAME = get_env_var("DYNAMO_DB_TABLE_NAME")


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


def handler(event, context):
    table = init_dynamo_db_table()

    response, record_id = create_lambda_status_record(table, "test", LambdaExecutionStatuses.IN_PROGRESS)
    print(response)
    print(record_id)
    response = update_record_status(table, LambdaExecutionStatuses.SUCCESS, "test", record_id)
    print(response)
    return "success"
