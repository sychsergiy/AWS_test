import boto3
import time
import uuid


class LambdaExecutionStatuses(object):
    FAILED_TO_INIT = "FAILED_TO_INIT"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"


def create_record_data(lambda_name, status):
    lambda_id = uuid.uuid4()

    now = int(time.time())
    return {
        "lambda_name": lambda_name,
        "date_started": now,
        "execution_status": status,
        "uuid": str(lambda_id),
    }


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


def init_dynamo_db_table():
    table_name = "LambdaExecutionState"
    dynamo_db = boto3.resource("dynamodb")
    return dynamo_db.Table(table_name)


def handler(event, context):
    dynamo_db_table = init_dynamo_db_table()
    record = create_record_data("test_lambda", LambdaExecutionStatuses.SUCCESS)
    dynamo_db_table.put_item(Item=record)
    update_record_status(
        dynamo_db_table, LambdaExecutionStatuses.FAILED, "test_lambda", record['uuid']
    )
