import click
import requests
from spc.utils.token import load_token
from spc.config import API_BASE_URL

@click.command(help="Create a new AWS container.")
@click.option('--requested_cpu', type=float, prompt=True, help="Requested CPU")
@click.option('--container_name', prompt=True, help="Container Name")
@click.option('--requested_storage', type=int, prompt=True, help="Requested Storage in GB")
def create_container(requested_cpu, requested_type, container_name, requested_storage):
    """Create a new AWS container."""
    token = load_token()
    if not token:
        click.echo('No valid token found. Please login first.')
        return

    response = requests.post(f'{API_BASE_URL}/api/aws/create_container', 
                             headers={'Authorization': f'Bearer {token}'}, 
                             json={
                                 'cpu': requested_cpu,
                                 'container_name': container_name,
                                 'storage': requested_storage
                             })

    if response.status_code == 200:
        click.echo('Container created successfully.')
    else:
        click.echo('Failed to create container.')
