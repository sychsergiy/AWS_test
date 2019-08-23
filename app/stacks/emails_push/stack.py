from troposphere import Template

from stacks.emails_push.resources import emails_sns_topic

template = Template()
template.add_parameter(emails_sns_topic)
