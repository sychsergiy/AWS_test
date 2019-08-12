import logging
import pymysql

logger = logging.getLogger()
logger.setLevel(logging.INFO)

rds_host = "mysqlforlambdatest.ct0xb8em3m2k.eu-central-1.rds.amazonaws.com"
username = "postgres"
password = "postgres"
name = "awstest"


def init_rds():
    try:
        connection = pymysql.connect(rds_host, user=username, passwd=password, db=name, connect_timeout=2)
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
