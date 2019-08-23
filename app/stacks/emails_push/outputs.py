from troposphere import Output, Export, Ref
from stacks.emails_push.resources import emails_sns_topic

STACK_NAME = "EmailsPush"

emails_sns_topic_ref_output_name = "EmailsSNSTopicRef"
emails_sns_topic_ref_export_name = "{}-{}".format(
    STACK_NAME, emails_sns_topic_ref_output_name
)
emails_sns_topic_ref_output = Output(
    emails_sns_topic_ref_output_name,
    Value=Ref(emails_sns_topic),
    Export=Export(emails_sns_topic_ref_export_name),
)
