from troposphere import (
    s3,
    Ref,
)

from resources.bucket_updates_topic import bucket_updates_topic

s3_bucket = s3.Bucket(
    "S3Bucket",
    NotificationConfiguration=s3.NotificationConfiguration(
        TopicConfigurations=[
            s3.TopicConfigurations(
                Event="s3:ObjectCreated:*",
                Topic=Ref(bucket_updates_topic)
            )
        ]
    )
)
