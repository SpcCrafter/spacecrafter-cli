import click
import requests
from getpass import getpass
from spc.utils.validators import validate_email
from spc.config import API_BASE_URL

@click.command(help="Sign up a new user with a username and email.")
@click.argument('username', type=str)
@click.argument('email', type=str)
def signup(username, email):
    """Sign up a new user."""
    if not validate_email(email):
        click.echo('Invalid email address.')
        return

    password = getpass('Password: ')
    confirm_password = getpass('Confirm Password: ')

    if password != confirm_password:
        click.echo('Passwords do not match.')
        return

    response = requests.post(f'{API_BASE_URL}/api/signup', json={
        'username': username,
        'email': email,
        'password': password
    })

    if response.status_code == 200:
        click.echo('Signup successful.')
    else:
        click.echo('Signup failed.')


