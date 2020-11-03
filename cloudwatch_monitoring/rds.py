"""
module for creating rds widgets

"""

import boto3

def create_rds_widgets(region, deploy_stage):

    rds_client = boto3.client("rds", region_name=region)

    """
    response = client.describe_db_instances(
        DBInstanceIdentifier='string',
        Filters=[
            {
                'Name': 'string',
                'Values': [
                    'string',
                ]
            },
        ],
        MaxRecords=123,
        Marker='string'
        )
    """

    rds_metadata = rds_client.describe_db_instances(
        Filters=[{
            'Name': 'wma:organization',
            'Values': [
                'IOW'
            ]
        }]
    )

    print(rds_metadata)
