import logging
import pg8000

from services.config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def init_rds():
    try:
        connection = pg8000.connect(
            host=Config.DB_HOST, port=int(Config.DB_PORT),
            user=Config.DB_USER, password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
        create_record_table(connection)
        return connection
    except pg8000.Error as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        return None


def create_record_table(connection):
    with connection.cursor() as cursor:
        create_record_table_query = """
            create table if not exists Record(
                id  serial PRIMARY KEY,
                bucket_name varchar(255),
                updated_file_name varchar(255) ,
                date_created TIMESTAMPTZ DEFAULT NOW()
            )
        """
        cursor.execute(create_record_table_query)
    connection.commit()


def insert_record_to_rds(cursor, bucket_name, updated_file_name):
    cursor.execute(
        "INSERT INTO Record (bucket_name, updated_file_name) VALUES (%s, %s);",
        (bucket_name, updated_file_name)

    )
