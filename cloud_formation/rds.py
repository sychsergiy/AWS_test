import logging

from services.rds import (
    init_rds,
    insert_record_to_rds,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    rds_connection = init_rds()
    if not rds_connection:
        return "Failed to connect to RDS"

    source_s3 = event['Records'][0]['s3']
    source_bucket_name, updated_file_name = source_s3['bucket']['name'], source_s3['object']['key']

    with rds_connection.cursor() as cursor:
        insert_record_to_rds(cursor, source_bucket_name, updated_file_name)
        rds_connection.commit()

    return "Inserted record with updated_file_name: %s" % updated_file_name
