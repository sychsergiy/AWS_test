from troposphere import ImportValue

from main.outputs import lambda_security_group_export_name

sns_topic_source_security_group = ImportValue(lambda_security_group_export_name)
