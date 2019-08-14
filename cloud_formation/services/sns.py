import boto3
import logging

from services.config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
