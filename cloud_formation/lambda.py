import time
import uuid
import boto3
import logging
import os
import pymysql

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_env_var(var_name, required=True):
    value = os.environ.get(var_name)
    if required:
        if not value:
            raise Exception("Env var: {} is required".format(var_name))
    return value


class Config(object):
    DB_NAME = get_env_var("DB_NAME")
    DB_USER = get_env_var("DB_USER")
    DB_PASSWORD = get_env_var("DB_PASSWORD")
    DB_HOST = get_env_var("DB_HOST")

    SNS_TOPIC_ARN = get_env_var("SNS_TOPIC_ARN")

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


def init_rds():
    try:
        connection = pymysql.connect(
            Config.DB_HOST, user=Config.DB_USER, passwd=Config.DB_PASSWORD, db=Config.DB_NAME, connect_timeout=2
        )
        logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
        create_record_table(connection)
        return connection
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        return None


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
        return "Failed to connect to DynamoDB"
    _, record_id = create_lambda_status_record(
        dynamo_db_table, lambda_name, LambdaExecutionStatuses.INITIALIZATION
    )

    rds_connection = init_rds()
    if not rds_connection:
        create_lambda_status_record(dynamo_db_table, lambda_name, LambdaExecutionStatuses.FAILED_TO_INIT)
        return "Failed to connect to RDS"

    update_record_status(
        dynamo_db_table, LambdaExecutionStatuses.IN_PROGRESS, lambda_name, record_id
    )

    source_s3 = event['Records'][0]['s3']
    source_bucket_name, updated_file_name = source_s3['bucket']['name'], source_s3['object']['key']

    with rds_connection.cursor() as cursor:
        insert_record_to_rds(cursor, source_bucket_name, updated_file_name)
        rds_connection.commit()

    return "Inserted record with updated_file_name: %s" % updated_file_name
