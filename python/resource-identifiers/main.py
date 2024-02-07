import boto3

# import json
import pandas as pd
from os import environ
from dynamodb import main as dynamodb
from functions import main as functions

# from s3 import main as s3
from ec2 import main as ec2


class Config:
    MANDATORY_TAGS = {
        'map-migrated': environ.get('MAP_MIGRATED_VALUE', 'd-example-asdfasdfasdf1232342345')
    }


def account_settings():
    """
    18-JAN-2024: Only supports listing available regions for the account.
    """
    client = boto3.client("account")
    list_regions = client.list_regions(RegionOptStatusContains=['ENABLED', 'ENABLED_BY_DEFAULT'])
    output = {'regions': [x['RegionName'] for x in list_regions['Regions']]}

    return output


def flatten_list(data):
    return [item for sublist in data for item in sublist]


def main():
    regions = account_settings()['regions']  # ['us-east-2']
    services = flatten_list(
        dynamodb(regions=regions)
        + ec2(regions=regions)
        + functions(regions=regions)
        # s3(regions=regions) +  # TODO - unable to add new tags to already tagged buckets (washingtonpost/aws-tagger)
    )

    # print(json.dumps(services, indent=4))

    output = []
    for x in services:
        x.update(Config.MANDATORY_TAGS)
        output.append(x)

    df = pd.DataFrame.from_records(output).set_index('Id')
    df.to_csv('tags.csv')
    print(df)


if __name__ == '__main__':
    main()
