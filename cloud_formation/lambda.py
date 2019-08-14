import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_env_var(var_name, required=True):
    value = os.environ.get(var_name)
    if required:
        if not value:
            raise Exception("Env var: {} is required".format(var_name))
    return value


class Config(object):
    SNS_TOPIC_ARN = get_env_var("SNS_TOPIC_ARN")


def send_message_to_email_topic(message):
    try:
        sns = boto3.client('sns')
        response = sns.publish(
            TopicArn=Config.SNS_TOPIC_ARN,
            Message=message,
        )
        logger.info(response)
        return True
    except Exception as e:
        logger.error("ERROR: Failed to send email message")
        logger.error(e)
        return False


def handler(event, context):
    return send_message_to_email_topic("HELLO WORLD")
