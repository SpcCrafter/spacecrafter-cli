import click
from spc.commands.signup import signup
from spc.commands.login import login
from spc.commands.set_aws_credentials import set_aws_credentials
from spc.commands.create_container import create_container

@click.group()
def cli():
    """Command Line Interface for Spacecrafter."""
    pass

cli.add_command(signup)
cli.add_command(login)
cli.add_command(set_aws_credentials)
cli.add_command(create_container)

if __name__ == '__main__':
    cli()
