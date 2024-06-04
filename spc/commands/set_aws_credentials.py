import click
import requests
from spc.utils.token import load_token
from spc.config import API_BASE_URL

@click.command(help="Set AWS credentials.")
@click.option('--aws_access_key_id', prompt=True, hide_input=True, help="AWS Access Key ID")
@click.option('--aws_secret_access_key', prompt=True, hide_input=True, help="AWS Secret Access Key")
@click.option('--preferred_aws_region', default='eu-central-1', help="Preferred AWS Region")
def set_aws_credentials(aws_access_key_id, aws_secret_access_key, preferred_aws_region):
    """Set AWS credentials."""
    token = load_token()
    if not token:
        click.echo('No valid token found. Please login first.')
        return

    response = requests.post(f'{API_BASE_URL}/api/aws/credentials', 
                             headers={'Authorization': f'Bearer {token}'}, 
                             json={
                                 'aws_access_key_id': aws_access_key_id,
                                 'aws_secret_access_key': aws_secret_access_key,
                                 'preferred_aws_region': preferred_aws_region
                             })

    if response.status_code == 200:
        click.echo('AWS credentials set successfully.')
    else:
        click.echo('Failed to set AWS credentials.')



