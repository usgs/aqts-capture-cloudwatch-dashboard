import boto3
import json
import os

from cloudwatch_monitoring.lambdas import (create_lambda_widgets, create_lambda_memory_usage_widgets,
                                           create_ecosystem_switch_widgets)
from cloudwatch_monitoring.rds import create_rds_widgets
from cloudwatch_monitoring.sqs import create_sqs_widgets
from cloudwatch_monitoring.state_machine import create_state_machine_widgets
from cloudwatch_monitoring.sns import create_sns_widgets

# Entrypoint from the jenkins script
if __name__ == '__main__':
    """
    Create a cloudwatch dashboard with basic and custom widgets for
    monitoring performance of aqts-capture etl assets
    """

    region = 'us-west-2'
    deploy_stage = os.getenv('DEPLOY_STAGE')

    main_dashboard_widgets = []
    memory_usage_widgets = []
    ecosystem_switch_widgets = []

    # add widgets to main dashboard
    main_dashboard_widgets.extend(create_sqs_widgets(region, deploy_stage))
    main_dashboard_widgets.extend(create_rds_widgets(region, deploy_stage))
    main_dashboard_widgets.extend(create_state_machine_widgets(region, deploy_stage))
    main_dashboard_widgets.extend(create_sns_widgets(region, deploy_stage))
    main_dashboard_widgets.extend(create_lambda_widgets(region, deploy_stage))

    # add widgets to memory usage dashboard
    memory_usage_widgets.extend(create_lambda_memory_usage_widgets(region, deploy_stage))

    # add widgets to ecosystem switch dashboard
    ecosystem_switch_widgets.extend(create_ecosystem_switch_widgets(region, deploy_stage))

    # create the dashboard when the widget list is complete
    cloudwatch_client = boto3.client("cloudwatch", region_name=region)
    dashboard_body = {'widgets': main_dashboard_widgets}
    dashboard_body_json = json.dumps(dashboard_body)
    cloudwatch_client.put_dashboard(DashboardName="aqts-capture-etl-" + deploy_stage, DashboardBody=dashboard_body_json)
