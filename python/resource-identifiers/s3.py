import boto3
from botocore.exceptions import ClientError


def _list_s3_buckets(client, region: str):
    """
    Gets a list of S3 buckets for an account in all enabled regions
    """

    tables = []
    try:
        __buckets = client.list_buckets()

        for info in __buckets['Buckets']:
            tables.append({'Region': region, 'Id': info['Name']})

    except ClientError as e:
        if 'explicit deny' in str(e):
            print(f'Explicit deny in place for {region}, unable to list S3 buckets...')

    return tables


def main(regions: list[str]):
    buckets = []
    for region in regions:
        client = boto3.client('s3', region_name=region)

        ## get the available s3 buckets for the different regions
        buckets.append(_list_s3_buckets(client, region=region))

    return buckets
