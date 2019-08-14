import os


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
