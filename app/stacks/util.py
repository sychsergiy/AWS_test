from troposphere import Template


def template_factory(parameters, resources, outputs):
    t = Template()
    for param in parameters:
        t.add_parameter(param)
    for resource in resources:
        t.add_resource(resource)
    for output in outputs:
        t.add_output(output)
    return t
