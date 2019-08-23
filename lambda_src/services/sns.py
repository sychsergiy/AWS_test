import logging

from config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_message_to_email_topic(sns_client, message):
    try:
        response = sns_client.publish(
            TopicArn=Config.SNS_TOPIC_ARN, Message=message
        )
        logger.info(response)
        return True
    except Exception as e:
        logger.error("ERROR: Failed to send email message")
        logger.error(e)
        return False
