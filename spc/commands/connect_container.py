import os
import sys
import click
import tempfile
import requests
import boto3
from spc.utils.token import load_token
from spc.config import API_BASE_URL

@click.command(help="Connect to an AWS container.")
@click.argument('container_name', type=str)
def connect_container(container_name):
    """Connect to an AWS container."""
    token = load_token()
    if not token:
        click.echo('No valid token found. Please login first.')
        return

    response = requests.post(f'{API_BASE_URL}/api/aws/container_connect', 
                             headers={'Authorization': f'Bearer {token}'}, 
                             json={'container_name': container_name})

    if response.status_code != 200:
        click.echo(f'Failed to connect to container: {response.json().get("message", "Unknown error")}')
        return

    data = response.json()
    public_ip = data['public_ip']
    s3_file_path = data['s3_file_path']
    aws_access_key_id = data['aws_access_key_id']
    aws_secret_access_key = data['aws_secret_access_key']
    preferred_aws_region = data['preferred_aws_region']

    # Download the key pair locally
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=preferred_aws_region
    )
    s3 = session.client('s3')
    kms = session.client('kms')

    # Parse the S3 file path
    bucket_name, key_name = s3_file_path.replace("s3://", "").split("/", 1)
    local_key_path = f"/tmp/{container_name}_temp_key.pem"

    if os.path.exists(local_key_path):
        try:
            os.remove(local_key_path)
        except OSError as e:
            click.echo(f'Failed to remove existing key file: {e}')
            return

    try:
        encrypted_key = s3.get_object(Bucket=bucket_name, Key=key_name)['Body'].read()
        decrypted_key = kms.decrypt(CiphertextBlob=encrypted_key)['Plaintext']
        
        # with open(local_key_path, 'wb') as key_file:
        #     key_file.write(decrypted_key)
        # os.chmod(local_key_path, 0o400)  # Ensure the key file has the correct permissions
        
    # Create a unique temporary file to hold the key
        with tempfile.NamedTemporaryFile(delete=False) as key_file:
            local_key_path = key_file.name
            key_file.write(decrypted_key)
        os.chmod(local_key_path, 0o400)  # Ensure the key file has the correct permissions

        click.echo(f'Downloaded key pair to {local_key_path}')
    except Exception as e:
        click.echo(f'Failed to download key pair: {e}')
        return

    is_tty = sys.stdin.isatty() and sys.stdout.isatty()
    # SSH into the instance
    command = (
        f"ssh -i {local_key_path} ubuntu@{public_ip}"
        f" {'-t' if is_tty else ''}"
        f" -- 'docker exec -it {container_name} /bin/bash'"
    )    
    os.system(command)
