from troposphere import (
    sns,
    Ref
)

from bucket_updates_topic import bucket_updates_topic

bucket_updates_topic_policy = sns.TopicPolicy(
    "BucketUpdatesTopicPolicy",
    PolicyDocument={
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "s3.amazonaws.com"
                },
                "Action": "sns:Publish",
                "Resource": "*"
            }
        ]
    },
    Topics=[Ref(bucket_updates_topic)]
)
