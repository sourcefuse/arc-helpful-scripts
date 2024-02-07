import boto3
import json


def settings():
    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

    output = {'regions': regions}

    return output


def aws_config_settings(regions):
    config_settings = []
    for region in regions:
        client = boto3.client('config', region_name=region)
        config_recorders = client.describe_configuration_recorders()['ConfigurationRecorders']
        delivery_channels = client.describe_delivery_channel_status()['DeliveryChannelsStatus']
        aggregation_authorizations = client.describe_aggregation_authorizations()[
            'AggregationAuthorizations'
        ]

        config_settings.append(
            {
                'region': region,
                'recorder_name': config_recorders[0]['name'] if len(config_recorders) > 0 else None,
                'delivery_channel_name': delivery_channels[0]['name']
                if len(delivery_channels) > 0
                else None,
            }
        )

    return config_settings


def delete_aws_config_settings(_settings):
    for setting in _settings:
        client = boto3.client('config', region_name=setting['region'])

        if setting['recorder_name'] is not None:
            client.stop_configuration_recorder(ConfigurationRecorderName=setting['recorder_name'])

        if setting['delivery_channel_name'] is not None:
            client.delete_delivery_channel(DeliveryChannelName=setting['delivery_channel_name'])

        if setting['recorder_name'] is not None:
            client.delete_configuration_recorder(ConfigurationRecorderName=setting['recorder_name'])


if __name__ == '__main__':
    regions = settings()['regions']
    # config_settings = json.dumps(aws_config_settings(regions=regions), indent=4)
    config_settings = aws_config_settings(regions=regions)

    # print(config_settings)

    delete_aws_config_settings(config_settings)
