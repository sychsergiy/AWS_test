from troposphere import Template

from stacks.parameters import email_address
from stacks.emails_push.resources import emails_sns_topic
from stacks.emails_push.outputs import emails_sns_topic_ref_output

template = Template()
template.add_parameter(email_address)
template.add_resource(emails_sns_topic)
template.add_output(emails_sns_topic_ref_output)
