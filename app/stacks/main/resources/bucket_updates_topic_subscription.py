from stacks.main.resources.lambda_handler import lambda_handler
from stacks.main.resources.bucket_updates_topic import bucket_updates_topic

from troposphere import sns, GetAtt, Ref

bucket_updates_topic_subscription = sns.SubscriptionResource(
    "BucketUpdatesTopicSubscription",
    Protocol="lambda",
    Endpoint=GetAtt(lambda_handler, "Arn"),
    TopicArn=Ref(bucket_updates_topic),
)
