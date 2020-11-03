"""
module for creating rds widgets

"""

import boto3
from .lookups import (rds_instances)

def create_rds_widgets(region, deploy_stage, positioning):

    observations = 'observations'
    nwcapture = 'nwcapture'

    rds_widgets = []

    observations_db_status_widget = generate_db_status_widget(region, deploy_stage, positioning, observations)
    nwcapture_db_status_widget = generate_db_status_widget(region, deploy_stage, positioning, nwcapture)

    rds_widgets.append(observations_db_status_widget)
    positioning.iterate_positioning()
    rds_widgets.append(nwcapture_db_status_widget)
    positioning.iterate_positioning()

    # TODO more custom widgets to follow

    return rds_widgets


def generate_db_status_widget(region, deploy_stage, positioning, db_name):

    db_properties = rds_instances[deploy_stage][db_name]

    db_status_widget = {
        'type': 'metric',
        'x': positioning.x,
        'y': positioning.y,
        'height': positioning.height + 3,
        'width': positioning.width,
        'properties': {
            "metrics": [
                ["AWS/RDS", "CPUUtilization", "DBInstanceIdentifier", db_properties['db_instance_identifier']],
                [".", "DatabaseConnections", ".", ".", {"yAxis": "right"}],
                ["...", db_properties['db_instance_identifier'], {"yAxis": "right"}],
                [".", "CPUUtilization", ".", "."]
            ],
            "view": "timeSeries",
            "stacked": False,
            "region": region,
            "title": f"{db_name.capwords()} DB Status",
            "period": 300,
            "stat": "Average",
        }
    }

    return db_status_widget
