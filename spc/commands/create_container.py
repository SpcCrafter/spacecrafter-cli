import click
import requests
from spc.utils.token import load_token
from spc.config import API_BASE_URL

@click.command(help="Create a new docker container.")
@click.argument('container_name', type=str)
@click.option('--cpu', type=float, prompt=True, help="Requested CPU")
@click.option('--storage', type=int, prompt=True, help="Requested Storage in MB")
@click.option('--image', prompt=True, help="Container Image")
@click.option('--env_vars', type=click.Path(exists=True), help="Path to environment variables file", default=None)
def create_container(container_name, cpu, storage, image, env_vars):
    """Create a new AWS container."""
    token = load_token()
    if not token:
        click.echo('No valid token found. Please login first.')
        return

    response = requests.post(f'{API_BASE_URL}/api/aws/create_container', 
                             headers={'Authorization': f'Bearer {token}'}, 
                             json={
                                 'container_name': container_name,
                                 'image': image,
                                 'cpu': cpu,
                                 'storage': storage,
                                 'env_vars': env_vars
                             })

    if response.status_code == 200:
        click.echo('Container created successfully.')
    else:
        click.echo('Failed to create container.')



