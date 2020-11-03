"""
module for creating rds widgets

"""

import boto3
from .lookups import (rds_instances)

def create_rds_widgets(region, deploy_stage, positioning):

    obs_db = 'observations'
    cap_db = 'nwcapture'
    db_id = 'db_instance_identifier'

    rds_widgets = []

    observations_db_status_widget = {
        'type': 'metric',
        'x': positioning.x,
        'y': positioning.y,
        'height': positioning.height + 3,
        'width': positioning.width,
        'properties': {
            "metrics": [
                ["AWS/RDS", "CPUUtilization", "DBInstanceIdentifier", rds_instances[deploy_stage][obs_db][db_id]],
                [".", "DatabaseConnections", ".", ".", {"yAxis": "right"}],
                ["...", rds_instances[deploy_stage][obs_db][db_id], {"yAxis": "right"}],
                [".", "CPUUtilization", ".", "."]
            ],
            "view": "timeSeries",
            "stacked": False,
            "region": region,
            "title": "Observations DB Status",
            "period": 300,
            "stat": "Average",
            "annotations": {
                "vertical": [
                    {
                        "label": "Added Index",
                        "value": "2020-04-10T15:30:00.000Z"
                    }
                ]
            }
        }
    }

    rds_widgets.append(observations_db_status_widget)
    positioning.iterate_positioning()

    # TODO more custom widgets to follow

    return rds_widgets
