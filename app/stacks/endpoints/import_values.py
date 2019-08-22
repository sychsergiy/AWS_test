from troposphere import ImportValue

from stacks.main.outputs import lambda_security_group_id_export_name

sns_topic_source_security_group_id = ImportValue(lambda_security_group_id_export_name)
