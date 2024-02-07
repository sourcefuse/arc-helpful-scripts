import boto3
from botocore.exceptions import ClientError


def _list_functions(client, region: str):
    """
    Gets a list of Lambda Functions for an account in all enabled regions
    """

    functions = []
    try:
        paginator = client.get_paginator('list_functions')
        for response in paginator.paginate():
            for arn in response['Functions']:
                functions.append({'Region': region, 'Id': arn['FunctionArn']})

    except ClientError as e:
        if 'explicit deny' in str(e):
            print(f'Explicit deny in place for {region}, unable to list functions...')

    return functions


def main(regions: list[str]):
    functions = []
    for region in regions:
        client = boto3.client('lambda', region_name=region)

        ## get the available lambda functions for the different regions
        functions.append(_list_functions(client, region=region))

    return functions
