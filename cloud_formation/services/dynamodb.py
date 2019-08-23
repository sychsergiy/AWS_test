import time
import uuid


class LambdaExecutionStatuses(object):
    INITIALIZATION = "INITIALIZATION"
    FAILED_TO_INIT = "FAILED_TO_INIT"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"


class DynamoDBTable(object):
    def __init__(self, table):
        self.table = table

    def create_lambda_status_record(self, lambda_name, status):
        record_id = str(uuid.uuid4())

        now = int(time.time())
        data = {
            "lambda_name": lambda_name,
            "date_started": now,
            "execution_status": status,
            "uuid": record_id,
        }
        return self.table.put_item(Item=data), record_id

    def update_record_status(self, status, lambda_name, record_id):
        response = self.table.update_item(
            Key={
                'lambda_name': lambda_name,
                'uuid': record_id,
            },
            UpdateExpression="set execution_status = :r",
            ExpressionAttributeValues={':r': status},
            ReturnValues="UPDATED_NEW"
        )
        return response
