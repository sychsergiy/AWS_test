from troposphere import ImportValue

from stacks.emails_push.outputs import emails_sns_topic_ref_export_name

emails_sns_topic = ImportValue(emails_sns_topic_ref_export_name)
