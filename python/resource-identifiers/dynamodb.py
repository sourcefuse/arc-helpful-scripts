import boto3
from botocore.exceptions import ClientError


def _list_tables(client, region: str):
    """
    Gets a list of DynamoDB tables for an account in all enabled regions
    """

    tables = []
    try:
        paginator = client.get_paginator('list_tables')
        table_names = []
        for response in paginator.paginate():
            for names in response['TableNames']:
                table_names.append(names)

        tables.append({'Region': region, 'tables': table_names})

    except ClientError as e:
        if 'explicit deny' in str(e):
            print(f'Explicit deny in place for {region}, unable to list DynamoDB tables...')

    return tables


def _table_info(client, tables: list[dict[str]]):
    """
    Gets the configuration details of the DynamoDB table and populates a dictionary for downstream use.
    """

    table_info = []
    for _details in tables:
        try:
            for table in _details['tables']:
                describe = client.describe_table(TableName=table)

                table_info.append(
                    {'Region': _details['Region'], 'Id': describe['Table']['TableArn']}
                )

        except ClientError as e:
            if 'explicit deny' in str(e):
                print(
                    f'Explicit deny in place for {_details["Region"]}, unable to retrieve info for DynamoDB tables...'
                )

    return table_info


def _list_global_tables(client, region: str):
    """
    Gets a list of DynamoDB Global table names for an account in all enabled regions
    """

    tables = []
    try:
        __tables = client.list_global_tables(RegionName=region)

        for info in __tables['GlobalTables']:
            tables.append({'Region': region, 'global_table_name': info['GlobalTableName']})

    except ClientError as e:
        if 'explicit deny' in str(e):
            print(f'Explicit deny in place for {region}, unable to list global DynamoDB tables...')

    return tables


def _global_table_info(client, tables: list[dict[str]]):
    """
    Gets the configuration details of the Global DynamoDB table and populates a dictionary for downstream use.
    """

    table_info = []
    for _details in tables:
        try:
            describe = client.describe_global_table(GlobalTableName=_details['global_table_name'])

            table_info.append(
                {
                    'Region': _details['Region'],
                    'Id': describe['GlobalTableDescription']['GlobalTableArn'],
                }
            )

        except ClientError as e:
            if 'explicit deny' in str(e):
                print(
                    f'Explicit deny in place for {_details["Region"]}, '
                    f'unable to retrieve global DynamoDB table info...'
                )

    return table_info


def main(regions: list[str]):
    tables = []
    for region in regions:
        client = boto3.client('dynamodb', region_name=region)

        ## get the available tables
        regional_tables = _list_tables(client, region=region)
        global_tables = _list_global_tables(client, region=region)

        ## get the table info
        table_info = _table_info(client, tables=regional_tables)
        global_info = _global_table_info(client, tables=global_tables)

        tables.append(table_info + global_info)

    return tables
