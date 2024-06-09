import json
import click
import requests
from getpass import getpass
from spc.utils.token import save_token
from spc.config import API_BASE_URL

@click.command(help="Log in a user with a username.")
@click.argument('username', type=str)
def login(username):
    """Log in a user."""
    password = getpass('Password: ')

    response = requests.post(f'{API_BASE_URL}/api/login', json={
        'username': username,
        'password': password
    })

    if response.status_code == 200:
        token = response.json().get('access_token')
        save_token(token)
        click.echo('Login successful.')
    else:
        try:
            message = response.json().get('message', 'Unknown error')
        except json.JSONDecodeError:
            message = 'Failed to parse error message from response.'
        
        click.echo(f'Login failed: {message}')
