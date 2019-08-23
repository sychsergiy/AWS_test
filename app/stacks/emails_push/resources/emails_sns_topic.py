from troposphere import sns, Ref

from stacks.parameters import email_address

emails_sns_topic = sns.Topic(
    "EmailsSNSTopic",
    Subscription=[
        sns.Subscription(Endpoint=Ref(email_address), Protocol="email")
    ],
)
