import sys
import logging
import pymysql

# rds settings
rds_host = "mysqlforlambdatest.ct0xb8em3m2k.eu-central-1.rds.amazonaws.com"
username = "postgres"
password = "postgres"
name = "awstest"
logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=username, passwd=password, db=name, connect_timeout=2)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


def handler(event, context):
    """
    This function fetches content from MySQL RDS instance
    """

    updated_file_text = "some text"
    with conn.cursor() as cur:
        create_record_table_query = """
        create table if not exists Record(
            id  int NOT NULL AUTO_INCREMENT,
            text varchar(255) NOT NULL,
            date_created datetime DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
        )
        """
        cur.execute(create_record_table_query)
        cur.execute('insert into Record (text) values("%(text)s")', {"text": updated_file_text})
        conn.commit()
    conn.commit()

    return "Inserted record with text: %s" % updated_file_text
