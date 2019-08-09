import sys
import logging
import pymysql

rds_host = "mysqlforlambdatest.ct0xb8em3m2k.eu-central-1.rds.amazonaws.com"
username = "postgres"
password = "postgres"
name = "awstest"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def init_rds():
    try:
        connection = pymysql.connect(rds_host, user=username, passwd=password, db=name, connect_timeout=2)
        logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
        return connection
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit()


def handler(event, context):
    conn = init_rds()
    source_s3 = event['Records'][0]['s3']
    source_bucket_name = source_s3['bucket']['name']
    updated_file_name = source_s3['object']['key']

    updated_file_text = "some text"
    with conn.cursor() as cur:
        create_record_table_query = """
        create table if not exists Record(
            id  int NOT NULL AUTO_INCREMENT,
            bucket_name varchar (255) NOT NULL,
            updated_file_name varchar (255) NOT NULL ,
            date_created datetime DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
        )
        """
        cur.execute(create_record_table_query)
        cur.execute(
            'insert into Record (bucket_name, updated_file_name) values("%(bucket_name)s", "%(updated_file_name)s")',
            {"bucket_name": source_bucket_name, "updated_file_name": updated_file_name}
        )
        cur.execute("select * from Record")
        for row in cur:
            logger.info(row)
    conn.commit()
    return "Inserted record with text: %s" % updated_file_text
