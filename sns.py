import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_message_to_email_topic(message):
    try:
        sns = boto3.client('sns')
        response = sns.publish(
            TopicArn='arn:aws:sns:eu-central-1:197928842860:email_lambda_finished',
            Message=message,
        )
        logger.info(response)
        return True
    except Exception as e:
        logger.error("ERROR: Failed to send email message")
        logger.error(e)
        return False
