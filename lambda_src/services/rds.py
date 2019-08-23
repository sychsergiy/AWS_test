import logging

import pg8000

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class PostgresDB(object):
    def __init__(self, connection):
        self.connection = connection

    def migrate(self):
        with self.connection.cursor() as cursor:
            create_record_table_query = """
                create table if not exists Record(
                    id  serial PRIMARY KEY,
                    bucket_name varchar(255),
                    updated_file_name varchar(255) ,
                    date_created TIMESTAMPTZ DEFAULT NOW()
                )
            """
            cursor.execute(create_record_table_query)
        self.connection.commit()

    def insert_record(self, bucket_name, updated_file_name):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Record (bucket_name, updated_file_name) VALUES (%s, %s);",
                (bucket_name, updated_file_name)
            )


def connect_to_postgres(config):
    try:
        connection = pg8000.connect(
            host=config.DB_HOST, port=int(config.DB_PORT),
            user=config.DB_USER, password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
        return connection
    except pg8000.Error as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        return None
