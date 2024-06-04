import click
import requests
from spc.utils.token import load_token
from spc.config import API_BASE_URL

@click.command(help="Delete a docker container.")
@click.argument('container_name', type=str)
def delete_container(container_name):
    """Delete an AWS container."""
    token = load_token()
    if not token:
        click.echo('No valid token found. Please login first.')
        return

    response = requests.delete(f'{API_BASE_URL}/api/aws/delete_container/{container_name}', 
                               headers={'Authorization': f'Bearer {token}'})

    if response.status_code == 200:
        click.echo('Container deleted successfully.')
    else:
        click.echo('Failed to delete container.')


