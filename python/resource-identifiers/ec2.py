import boto3
from botocore.exceptions import ClientError


def _list_instances(region: str):
    """
    Gets a list of EC2 instances for an account in all enabled regions
    """

    instances = []
    try:
        session = boto3.Session(region_name=region)
        ec2 = session.resource('ec2')
        _instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped']}]
        )
        for instance in _instances:
            instances.append({'Region': region, 'Id': instance.id})

    except ClientError as e:
        if 'explicit deny' in str(e):
            print(f'Explicit deny in place for {region}, unable to list EC2 instance Ids...')

    return instances


def main(regions: list[str]):
    instances = []
    for region in regions:
        ## get the available ec2 instances for the different regions
        instances.append(_list_instances(region=region))

    return instances
