import logging
import pymysql
import boto3
import time
import uuid

rds_host = "mysqlforlambdatest.ct0xb8em3m2k.eu-central-1.rds.amazonaws.com"
username = "postgres"
password = "postgres"
name = "awstest"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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


def init_dynamo_db_table():
    try:
        table_name = "LambdaExecutionState"
        dynamo_db = boto3.resource("dynamodb")
        table = dynamo_db.Table(table_name)
        return table
    except Exception as e:
        logger.error("ERROR: Failed to init DynamoDB")
        logger.error(e)
        return None


def init_rds():
    try:
        connection = pymysql.connect(rds_host, user=username, passwd=password, db=name, connect_timeout=2)
        logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
        return connection
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        return None


def send_message_to_email_topic():
    sns = boto3.client('sns')
    response = sns.publish(
        TopicArn='arn:aws:sns:eu-central-1:197928842860:email_lambda_finished',
        Message='Hello World!',
    )
    return response


def create_record_table(connection):
    with connection.cursor() as cursor:
        create_record_table_query = """
            create table if not exists Record(
                id  int NOT NULL AUTO_INCREMENT,
                bucket_name varchar (255) NOT NULL,
                updated_file_name varchar (255) NOT NULL ,
                date_created datetime DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id)
            )
            """
        cursor.execute(create_record_table_query)
    connection.commit()


def insert_record_to_rds(cursor, bucket_name, updated_file_name):
    cursor.execute(
        'insert into Record (bucket_name, updated_file_name) values("%(bucket_name)s", "%(updated_file_name)s")',
        {"bucket_name": bucket_name, "updated_file_name": updated_file_name}
    )


def handler(event, context):
    lambda_name = "aws_test"
    dynamo_db_table = init_dynamo_db_table()
    if not dynamo_db_table:
        return
    _, record_id = create_lambda_status_record(
        dynamo_db_table, lambda_name, LambdaExecutionStatuses.INITIALIZATION
    )

    rds_connection = init_rds()
    if not rds_connection:
        create_lambda_status_record(dynamo_db_table, lambda_name, LambdaExecutionStatuses.FAILED_TO_INIT)
        return

    update_record_status(
        dynamo_db_table, LambdaExecutionStatuses.IN_PROGRESS, lambda_name, record_id
    )

    source_s3 = event['Records'][0]['s3']
    source_bucket_name, updated_file_name = source_s3['bucket']['name'], source_s3['object']['key']

    with rds_connection.cursor() as cursor:
        insert_record_to_rds(cursor, source_bucket_name, updated_file_name)
        rds_connection.commit()

    try:
        response = send_message_to_email_topic()
        logger.info(response)
        update_record_status(
            dynamo_db_table, LambdaExecutionStatuses.SUCCESS, lambda_name, record_id
        )
    except Exception as e:
        logger.error("ERROR: Failed to send email message")
        logger.error(e)
        update_record_status(
            dynamo_db_table, LambdaExecutionStatuses.FAILED, lambda_name, record_id
        )

    return "Inserted record with updated_file_name: %s" % updated_file_name
