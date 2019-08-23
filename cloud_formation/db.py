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
