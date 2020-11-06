"""
module for creating rds widgets

"""

import boto3
from .lookups import (rds_instances)


def create_rds_widgets(region, deploy_stage, positioning):
    """
    Creates the list of RDS widgets.

    :param region: Typically 'us-west-2'
    :param deploy_stage: The deploy tier, DEV, TEST, QA, PROD-EXTERNAL
    :param positioning: The x, y, height, width coordinates and dimensions on the dashboard
    :return: list of RDS widgets
    :rtype: list
    """
    rds_widgets = []

    # db status widgets, cpu utilization and number of db connections
    for db_name in rds_instances:
        rds_widgets.append(generate_db_status_widget(region, deploy_stage, positioning, db_name))

    return rds_widgets


def generate_db_status_widget(region, deploy_stage, positioning, db_name):
    """
    Generates database status widgets, specifically for cpu utilization and number of database connections.

    :param region: Typically 'us-west-2'
    :param deploy_stage: The deploy tier, DEV, TEST, QA, PROD-EXTERNAL
    :param positioning: The x, y, height, width coordinates and dimensions on the dashboard
    :param db_name: observations or nwcapture
    :return: A db status widget
    :rtype: dict
    """

    db_properties = rds_instances[db_name][deploy_stage]
    db_identifier_type = rds_instances[db_name]['identifier_type']

    # set dimensions of the rds widgets
    positioning.width = 12
    positioning.height = 6

    db_status_widget = {
        'type': 'metric',
        'x': positioning.x,
        'y': positioning.y,
        'height': positioning.height,
        'width': positioning.width,
        'properties': {
            "metrics": [
                ["AWS/RDS", "CPUUtilization", db_identifier_type, db_properties['identifier']],
                [".", "DatabaseConnections", ".", ".", {"yAxis": "right"}]
            ],
            "view": "timeSeries",
            "stacked": False,
            "region": region,
            "title": f"{db_name.capitalize()} DB Status",
            "period": 300,
            "stat": "Average",
        }
    }

    positioning.iterate_positioning()
    return db_status_widget
