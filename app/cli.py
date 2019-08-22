import click

from stacks.endpoints.stack import template as endpoints_stack_template
from stacks.main.stack import template as main_stack_template


def write_file_from_template(file_name, template):
    path = "templates/{}".format(file_name)
    with open(path, "w") as f:
        f.write(template.to_yaml())


@click.group()
def cli():
    pass


@cli.command()
def generate_main_stack_template():
    write_file_from_template("main.yaml", main_stack_template)


@cli.command()
def generate_endpoints_stack_template():
    write_file_from_template("endpoints.yaml", endpoints_stack_template)


@cli.command()
def generate():
    write_file_from_template("main.yaml", main_stack_template)
    write_file_from_template("endpoints.yaml", endpoints_stack_template)


if __name__ == "__main__":
    cli()
